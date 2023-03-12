import re
from datetime import datetime

from app import schedule_service_v1, user_service_v1
from core.constants import BotState, MeetingFormat
from decorators import at
from handlers.handlers_utils import make_message_for_active_meeting
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from ui.buttons import BTN_START_MENU
from utils import make_message_handler, make_text_handler

from . import buttons
from .enums import States
from .helpers import context_manager
from .messages import (
    psychologist_meeting_message,
    user_check_meeting_message,
    user_choose_timeslot_message,
)
from .root_handlers import back_to_start_menu


def ask_for_repeat_meeting(state: str):
    @at
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        text = ""
        keyboard = None
        chat_data = update.message.chat
        telegram_login = chat_data.username

        user = user_service_v1.get_user(username=telegram_login)
        if user is None:
            text = "Ваших данных нет в базе"
            await update.message.reply_text(text=text, reply_markup=keyboard)
            return BotState.STOPPING

        user_active_meeting = schedule_service_v1.get_meetings_by_user(
            user=user.id, is_active="True"
        )
        if user_active_meeting:
            text = make_message_for_active_meeting(user_active_meeting)
            await update.message.reply_text(text=text)
            await back_to_start_menu(update, context)
            return BotState.STOPPING

        if state == States.TYPING_MEETING_FORMAT:
            text = "Выберите формат участия:"
            btns = [[buttons.BTN_MEETING_FORMAT_ONLINE, buttons.BTN_MEETING_FORMAT_OFFLINE]]
            keyboard = ReplyKeyboardMarkup(btns, one_time_keyboard=True)

        if state == States.TYPING_TIME_SLOT:
            meeting_format = update.message.text
            context_manager.set_meeting_format(context, meeting_format)

            meetings = schedule_service_v1.get_meetings_by_user(user=user.id, is_active="False")
            psycho_set = {meeting.psychologist for meeting in meetings}

            timeslots = schedule_service_v1.get_actual_timeslots(is_free="True")
            timeslots = sorted(timeslots, key=lambda x: (x.profile.id not in psycho_set))

            text = await user_choose_timeslot_message(timeslots, psycho_set)
            context_manager.set_timeslots(context, timeslots)

        if state == States.TYPING_MEETING_CONFIRM:
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

            btns = [[buttons.BTN_CONFIRM_MEETING, buttons.BTN_NOT_CONFIRM_MEETING]]
            keyboard = ReplyKeyboardMarkup(btns, one_time_keyboard=True)

        context_manager.set_user(context, user)

        await update.message.reply_text(text=text, reply_markup=keyboard)

        return state

    return inner


@at
async def go_to_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "выполняется переход на прохождение теста НДО:"
    await update.message.reply_text(text)
    return "---"


def process_meeting_confirm(confirm: bool):
    @at
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        if confirm:
            user = context_manager.get_user(context)
            timeslot = context_manager.get_timeslot(context)
            meeting_format = context_manager.get_meeting_format(context)
            schedule_service_v1.create_meeting(
                date_start=str(datetime.strptime(timeslot.date_start, "%d.%m.%Y %H:%M")),
                psychologist_id=timeslot.profile.id,
                user_id=user.id,
                meeting_format=MeetingFormat.MEETING_FORMAT_ONLINE
                if meeting_format == buttons.BTN_MEETING_FORMAT_ONLINE.text
                else MeetingFormat.MEETING_FORMAT_OFFLINE,
                timeslot=timeslot.id,
                comment="Повторная запись",
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
        make_message_handler(BTN_START_MENU, back_to_start_menu),
        # make_message_handler(BTN_ADMIN_MENU, back_to_admin),
        # make_message_handler(BTN_TESTS_MENU, menu_tests),
    ],
    map_to_parent={
        BotState.STOPPING: BotState.END,
        BotState.END: BotState.MENU_MEETING_SELECTING_LEVEL,
    },
)
