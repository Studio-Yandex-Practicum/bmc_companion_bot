from datetime import datetime

from app import schedule_service_v1, user_service_v1
from core.constants import BotState
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from utils import make_message_handler, make_text_handler

from . import buttons
from .enums import States
from .helpers import context_manager
from .root_handlers import back_to_start_menu


def ask_for_repeat_meeting(state: str):
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        text = ""
        keyboard = None
        chat_data = update.message.chat
        telegram_login = chat_data.username

        user = user_service_v1.get_user(username=telegram_login)
        if user is None:
            text = "Ваших данных нет в базе"
            await update.message.reply_text(text=text, reply_markup=keyboard)
            return BotState.MENU_START_SELECTING_LEVEL

        if state == States.TYPING_MEETING_FORMAT:
            text = "Выберите формат участия:"
            btns = [[buttons.BTN_MEETING_FORMAT_ONLINE, buttons.BTN_MEETING_FORMAT_OFFLINE]]
            keyboard = ReplyKeyboardMarkup(btns, one_time_keyboard=True)
        elif state == States.TYPING_TIME_SLOT:
            meeting_format = update.message.text
            context_manager.set_meeting_format(context, meeting_format)

            text = "Выберите дату и время записи:\n"
            timeslots = schedule_service_v1.get_actual_timeslots()

            for index, timeslot in enumerate(timeslots):
                if timeslot.date_start and timeslot.profile:
                    text += (
                        f"\n{index + 1}. {timeslot.profile.first_name} "
                        f"{timeslot.profile.last_name} "
                        f"{timeslot.date_start}"
                    )

            context_manager.set_timeslots(context, timeslots)

        elif state == States.TYPING_MEETING_CONFIRM:
            number_of_timeslot = int(update.message.text)
            meeting_format = context_manager.get_meeting_format(context)
            timeslots = context_manager.get_timeslots(context) or []
            timeslot = timeslots[number_of_timeslot - 1] if timeslots else {}

            context_manager.set_timeslot(context, timeslot)

            text = "Давайте все проверим:\n"
            text += f"\nФормат записи: {meeting_format}"
            text += f"\nПсихолог: {timeslot.profile.first_name} {timeslot.profile.last_name}"
            text += f"\nДата: {timeslot.date_start}"

            btns = [[buttons.BTN_CONFIRM_MEETING, buttons.BTN_NOT_CONFIRM_MEETING]]
            keyboard = ReplyKeyboardMarkup(btns, one_time_keyboard=True)

        context_manager.set_user(context, user)

        await update.message.reply_text(text=text, reply_markup=keyboard)

        return state

    return inner


async def go_to_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "выполняется переход на прохождение теста НДО:"
    await update.message.reply_text(text)
    return "---"


def process_meeting_confirm(confirm: bool):
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        if confirm:
            user = context_manager.get_user(context)
            timeslot = context_manager.get_timeslot(context)
            meeting_format = context_manager.get_meeting_format(context)
            schedule_service_v1.create_meeting(
                date_start=str(datetime.strptime(timeslot.date_start, "%d.%m.%Y %H:%M")),
                psychologist_id=timeslot.profile.id,
                user_id=user.id,
                meeting_format=10
                if meeting_format == buttons.BTN_MEETING_FORMAT_ONLINE.text
                else 20,
            )

            psychologist_chat_id = timeslot.profile.chat_id
            if psychologist_chat_id:
                meeting_text = (
                    f"У вас новая запись:\n\n"
                    f"кто: {user.first_name} {user.last_name}\n"
                    f"телефон: {user.phone}\n"
                    f"когда: {timeslot.date_start}\n"
                    f"где: {meeting_format}\n"
                )
                await context.bot.send_message(chat_id=psychologist_chat_id, text=meeting_text)

            text = "Вы успешно записаны к психологу!"
        else:
            text = "Запись не оформлена!"

        await update.message.reply_text(text=text)

        await back_to_start_menu(update, context)

        return BotState.STOPPING

    return inner


meeting_repeat_section = ConversationHandler(
    entry_points=[
        make_message_handler(
            buttons.BTN_MEETING_REPEAT, ask_for_repeat_meeting(States.TYPING_MEETING_FORMAT)
        ),
    ],
    states={
        States.TYPING_MEETING_FORMAT: [
            make_message_handler(
                buttons.BTN_MEETING_FORMAT_ONLINE, ask_for_repeat_meeting(States.TYPING_TIME_SLOT)
            ),
            make_message_handler(
                buttons.BTN_MEETING_FORMAT_OFFLINE, ask_for_repeat_meeting(States.TYPING_TIME_SLOT)
            ),
        ],
        States.TYPING_TIME_SLOT: [
            make_text_handler(ask_for_repeat_meeting(States.TYPING_MEETING_CONFIRM)),
        ],
        States.TYPING_MEETING_CONFIRM: [
            make_message_handler(buttons.BTN_CONFIRM_MEETING, process_meeting_confirm(True)),
            make_message_handler(buttons.BTN_NOT_CONFIRM_MEETING, process_meeting_confirm(False)),
        ],
    },
    fallbacks=[
        # make_message_handler(BTN_ADMIN_MENU, back_to_admin),
        # make_message_handler(BTN_TESTS_MENU, menu_tests),
    ],
    map_to_parent={
        BotState.STOPPING: BotState.END,
    },
)
