import re
from datetime import datetime

import phonenumbers
from app import schedule_service_v1, user_service_v1
from core.constants import DO_NOTHING_SIGN, BotState, MeetingFormat
from decorators import at, t
from handlers.handlers_utils import make_message_for_active_meeting
from handlers.questioning.root_handlers import api_client
from handlers.questioning.uce_test_selection import uce_test_section
from schemas.requests import UceTestRequest, UserTestSpecificRequest
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from ui.buttons import BTN_START_MENU
from utils import (
    make_ask_for_input_information,
    make_message_handler,
    make_text_handler,
)

from . import buttons
from .enums import States
from .helpers import context_manager
from .messages import (
    psychologist_meeting_message,
    user_check_meeting_message,
    user_choose_timeslot_message,
)
from .root_handlers import back_to_start_menu


@t
def ask_for_input(state: str):
    @at
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        text = ""
        keyboard = None
        chat_data = update.message.chat
        telegram_login = chat_data.username
        next_state = state

        user = user_service_v1.get_user(username=telegram_login)
        if not user:
            user = user_service_v1.create_user(
                telegram_login=telegram_login, first_name=chat_data.first_name, chat_id=chat_data.id
            )

        user_active_meeting = schedule_service_v1.get_meetings_by_user(
            user=user.id, is_active="True"
        )
        if user_active_meeting:
            text = make_message_for_active_meeting(user_active_meeting)
            await update.message.reply_text(text=text)
            await back_to_start_menu(update, context)
            return BotState.END

        timeslots = schedule_service_v1.get_actual_timeslots(is_free="True")
        if not timeslots:
            text = "Сейчас нет свободных слотов для записи. Попробуйте посмотреть завтра."
            await update.message.reply_text(text=text)
            await back_to_start_menu(update, context)
            return BotState.END

        timeslots = sorted(
            timeslots, key=lambda x: (datetime.strptime(x.date_start, "%d.%m.%Y %H:%M"))
        )

        if state == States.TYPING_PHONE:
            text = make_ask_for_input_information("Введите номер телефона", user.phone)
        elif state == States.TYPING_FIRST_NAME:
            text = make_ask_for_input_information(
                "Как Вас зовут? Введите только имя", user.first_name
            )
            phone = update.message.text
            if phone != DO_NOTHING_SIGN:
                try:
                    parsed_phone = phonenumbers.parse(phone, "RU")
                    if not phonenumbers.is_valid_number(parsed_phone):
                        raise ValueError
                    phone = phonenumbers.format_number(
                        parsed_phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL
                    )
                    user = user_service_v1.update_user(user.id, phone=phone)
                except (phonenumbers.NumberParseException, ValueError):
                    text = make_ask_for_input_information(
                        "Ваш номер телефона неверный, введите еще раз", user.phone
                    )
                    next_state = States.TYPING_PHONE

        elif state == States.TYPING_LAST_NAME:
            text = make_ask_for_input_information("Введите фамилию", user.last_name)
            first_name = update.message.text
            if first_name != DO_NOTHING_SIGN:
                if not first_name.isalpha():
                    text = make_ask_for_input_information(
                        "Имя не может содержать символы и цифры, введите еще раз", user.first_name
                    )
                    next_state = States.TYPING_FIRST_NAME
                else:
                    user = user_service_v1.update_user(user.id, first_name=first_name.title())

        elif state == States.TYPING_AGE:
            text = make_ask_for_input_information("Введите возраст", user.age)
            last_name = update.message.text
            if last_name != DO_NOTHING_SIGN:
                if not last_name.isalpha():
                    text = make_ask_for_input_information(
                        "Фамилия не может содержать символы и цифры, введите еще раз",
                        user.last_name,
                    )
                    next_state = States.TYPING_LAST_NAME
                else:
                    user = user_service_v1.update_user(user.id, last_name=last_name.title())

        elif state == States.TYPING_TEST_SCORE:
            text = make_ask_for_input_information("Введите свой балл за тест НДО", user.uce_score)
            age = update.message.text
            if age != DO_NOTHING_SIGN:
                if not age.isdigit():
                    text = make_ask_for_input_information(
                        "Возраст может быть только положительным и должен содержать только цифры",
                        user.age,
                    )
                    next_state = States.TYPING_AGE
                else:
                    user = user_service_v1.update_user(user.id, age=age)

            btns = [[buttons.BTN_I_DONT_KNOW]]
            keyboard = ReplyKeyboardMarkup(btns, resize_keyboard=True)

        elif state == States.TYPING_COMMENT:
            uce_score = update.message.text
            if uce_score != DO_NOTHING_SIGN and uce_score.isnumeric():
                user = user_service_v1.update_user(user.id, uce_score=uce_score)
            else:
                uce_test_id = api_client.uce_test_id(UceTestRequest()).id
                uce_test_result = api_client.test_result(
                    UserTestSpecificRequest(user_id=user.id, test_id=uce_test_id)
                )
                user = user_service_v1.update_user(user.id, uce_score=uce_test_result)
            text = "О чем бы вы хотели поговорить с психологом?"

            btns = [[buttons.BTN_I_DONT_KNOW]]
            keyboard = ReplyKeyboardMarkup(btns, resize_keyboard=True)

        elif state == States.TYPING_MEETING_FORMAT:
            comment = update.message.text
            context_manager.set_meeting_comment(context, comment)

            text = "Выберите формат участия:"
            btns = [[buttons.BTN_MEETING_FORMAT_ONLINE, buttons.BTN_MEETING_FORMAT_OFFLINE]]
            keyboard = ReplyKeyboardMarkup(btns, resize_keyboard=True)

        elif state == States.TYPING_TIME_SLOT:
            meeting_format = update.message.text
            context_manager.set_meeting_format(context, meeting_format)

            text = "Выберите дату и время записи:\n"
            timeslots = schedule_service_v1.get_actual_timeslots(is_free="True")

            text = await user_choose_timeslot_message(timeslots)

            context_manager.set_timeslots(context, timeslots)
            btns = [[buttons.BTN_NOT_CONFIRM_MEETING]]
            keyboard = ReplyKeyboardMarkup(btns, resize_keyboard=True)

        elif state == States.TYPING_MEETING_CONFIRM:
            number_of_timeslot = re.findall("\\d+", update.message.text) or []
            timeslots = context_manager.get_timeslots(context) or []
            if not number_of_timeslot or int(number_of_timeslot[0]) > len(timeslots):
                text = "Введен неправильный номер !\nНет таймслота под таким номером."
                await update.message.reply_text(text=text, reply_markup=keyboard)
                await back_to_start_menu(update, context)
                return BotState.STOPPING
            else:
                number_of_timeslot = int(number_of_timeslot[0])
            meeting_format = context_manager.get_meeting_format(context)
            timeslots = context_manager.get_timeslots(context) or []
            timeslot = timeslots[number_of_timeslot - 1] if timeslots else {}

            context_manager.set_timeslot(context, timeslot)

            text = await user_check_meeting_message(
                meeting_format,
                timeslot.profile.first_name,
                timeslot.profile.last_name,
                timeslot.date_start,
            )

            btns = [[buttons.BTN_CONFIRM_MEETING], [buttons.BTN_NOT_CONFIRM_MEETING]]
            keyboard = ReplyKeyboardMarkup(btns, resize_keyboard=True)

        context_manager.set_user(context, user)

        await update.message.reply_text(text=text, reply_markup=keyboard)

        return next_state

    return inner


def process_meeting_confirm(confirm: bool):
    @at
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        if confirm:
            user = context_manager.get_user(context)
            timeslot = context_manager.get_timeslot(context)
            meeting_format = context_manager.get_meeting_format(context)
            comment = context_manager.get_comment(context)
            schedule_service_v1.create_meeting(
                date_start=str(datetime.strptime(timeslot.date_start, "%d.%m.%Y %H:%M")),
                psychologist_id=timeslot.profile.id,
                user_id=user.id,
                comment=comment,
                meeting_format=MeetingFormat.MEETING_FORMAT_ONLINE
                if meeting_format == buttons.BTN_MEETING_FORMAT_ONLINE.text
                else MeetingFormat.MEETING_FORMAT_OFFLINE,
                timeslot=timeslot.id,
            )

            psychologist_chat_id = timeslot.profile.chat_id
            if psychologist_chat_id:
                meeting_text = await psychologist_meeting_message(meeting_format, user, timeslot)
                await context.bot.send_message(chat_id=psychologist_chat_id, text=meeting_text)

            text = "Вы успешно записаны к психологу!"
        else:
            text = "Запись не оформлена!"

        await update.message.reply_text(text=text)

        await back_to_start_menu(update, context)

        return BotState.STOPPING

    return inner


meeting_first_section = ConversationHandler(
    entry_points=[
        make_message_handler(buttons.BTN_MEETING_FIRST, ask_for_input(States.TYPING_PHONE)),
    ],
    states={
        States.TYPING_PHONE: [
            make_text_handler(ask_for_input(States.TYPING_FIRST_NAME)),
        ],
        States.TYPING_FIRST_NAME: [
            make_text_handler(ask_for_input(States.TYPING_LAST_NAME)),
        ],
        States.TYPING_LAST_NAME: [
            make_text_handler(ask_for_input(States.TYPING_AGE)),
        ],
        States.TYPING_AGE: [
            make_text_handler(ask_for_input(States.TYPING_TEST_SCORE)),
        ],
        States.TYPING_TEST_SCORE: [
            uce_test_section,
            make_text_handler(ask_for_input(States.TYPING_COMMENT)),
        ],
        States.TYPING_COMMENT: [
            make_text_handler(ask_for_input(States.TYPING_MEETING_FORMAT)),
        ],
        States.TYPING_MEETING_FORMAT: [
            make_message_handler(
                buttons.BTN_MEETING_FORMAT_ONLINE, ask_for_input(States.TYPING_TIME_SLOT)
            ),
            make_message_handler(
                buttons.BTN_MEETING_FORMAT_OFFLINE, ask_for_input(States.TYPING_TIME_SLOT)
            ),
        ],
        States.TYPING_TIME_SLOT: [
            make_text_handler(ask_for_input(States.TYPING_MEETING_CONFIRM)),
        ],
        States.TYPING_MEETING_CONFIRM: [
            make_message_handler(buttons.BTN_CONFIRM_MEETING, process_meeting_confirm(True)),
            make_message_handler(buttons.BTN_NOT_CONFIRM_MEETING, process_meeting_confirm(False)),
        ],
    },
    fallbacks=[
        # make_message_handler(BTN_ADMIN_MENU, back_to_admin),
        # make_message_handler(BTN_TESTS_MENU, menu_tests),
        make_message_handler(BTN_START_MENU, back_to_start_menu),
    ],
    map_to_parent={
        BotState.STOPPING: BotState.END,
        BotState.END: BotState.MENU_START_SELECTING_LEVEL,
    },
)
