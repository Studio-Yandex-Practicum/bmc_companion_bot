from datetime import datetime

from app import schedule_service_v1, user_service_v1
from core.constants import BotState, MeetingFormat
from handlers.meeting.root_handlers import back_to_start_menu
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from ui.buttons import BTN_START_MENU
from utils import context_manager as cm
from utils import make_message_handler, make_text_handler

from . import buttons
from .enums import States
from .helpers import context_manager


def ask_for_reschedule(state: str):
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        keyboard = None
        chat_data_id = update.message.chat.id
        user = user_service_v1.get_user(chat_id=chat_data_id)
        meetings = schedule_service_v1.get_meetings_by_user(chat_id=user.chat_id)
        timeslots = schedule_service_v1.get_actual_timeslots()

        if not meetings:
            text_parts = ["У вас нет записи"]
            button = [[BTN_START_MENU]]
            keyboard = ReplyKeyboardMarkup(button, one_time_keyboard=True)
            await update.message.reply_text(text="".join(text_parts), reply_markup=keyboard)
            await back_to_start_menu(update, context)
            return BotState.STOPPING

        if len(timeslots) < 2:
            text_parts = ["Извините, сейчас нет подходящего времени для переноса записи"]
            button = [[BTN_START_MENU]]
            keyboard = ReplyKeyboardMarkup(button, one_time_keyboard=True)
            await update.message.reply_text(text="".join(text_parts), reply_markup=keyboard)
            await back_to_start_menu(update, context)
            return BotState.STOPPING

        if state == States.TYPING_MEETING_FORMAT:
            text_parts = ["Выберите формат участия:"]
            btns = [[buttons.BTN_MEETING_FORMAT_ONLINE, buttons.BTN_MEETING_FORMAT_OFFLINE]]
            keyboard = ReplyKeyboardMarkup(btns, one_time_keyboard=True)

        if state == States.TYPING_TIME_SLOT:
            meeting_format = update.message.text
            context_manager.set_meeting_format(context, meeting_format)

            text_parts = ["Выберите новую дату:\n"]

            for index, timeslot in enumerate(timeslots, start=1):
                if timeslot.date_start and timeslot.profile:
                    text_parts.append(f"\n{index}. {timeslot.profile.first_name}")
                    text_parts.append(f"{timeslot.profile.last_name} ")
                    text_parts.append(f"{timeslot.date_start}")

            context_manager.set_timeslots(context, timeslots)

        if state == States.TYPING_MEETING_SLOT:
            number_of_timeslot = int(update.message.text)
            context_manager.set_timeslot_number(context, number_of_timeslot)

            text_parts = ["Выберите запись которую хотите перенести:\n"]

            for index, meeting in enumerate(meetings, start=1):
                psychologist_profile = user_service_v1.get_user(id=meeting.psychologist)
                text_parts.append(
                    f"\n{index}. {psychologist_profile.first_name} "
                    f"{psychologist_profile.last_name}"
                )
                text_parts.append(f"{meeting.date_start}")

        if state == States.TYPING_MEETING_CONFIRM:
            meeting_number = int(update.message.text)
            context_manager.set_meeting_number(context, meeting_number)
            meeting_format = context_manager.get_meeting_format(context)
            timeslots = context_manager.get_timeslots(context) or []
            number_of_timeslot = context_manager.get_timeslot_number(context)
            timeslot = timeslots[number_of_timeslot - 1] if timeslots else {}

            context_manager.set_timeslot(context, timeslot)

            text_parts = ["Давайте все проверим:\n"]
            text_parts += [f"\nФормат записи: {meeting_format}"]
            text_parts += [
                f"\nПсихолог: {timeslot.profile.first_name} {timeslot.profile.last_name}"
            ]
            text_parts += [f"\nДата: {timeslot.date_start}"]

            btns = [[buttons.BTN_CONFIRM_MEETING, buttons.BTN_NOT_CONFIRM_MEETING]]
            keyboard = ReplyKeyboardMarkup(btns, one_time_keyboard=True)

        context_manager.set_user(context, user)
        cm.set_meetings(context, meetings)

        if text_parts:
            await update.message.reply_text(text="".join(text_parts), reply_markup=keyboard)
        else:
            text = "Извините, попробуйте ещё раз"
            await update.message.reply_text(text=text)
            await back_to_start_menu(update, context)
            return BotState.STOPPING

        return state

    return inner


def meeting_update(confirm: bool):
    """Обновление записи пользователя"""

    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        if confirm:
            user = context_manager.get_user(context)
            timeslot = context_manager.get_timeslot(context)
            meeting_format = context_manager.get_meeting_format(context)
            meetings = cm.get_meetings(context)
            meeting_number = context_manager.get_meeting_number(context)
            meeting = meetings[meeting_number - 1]
            schedule_service_v1.update_meeting(
                date_start=str(datetime.strptime(timeslot.date_start, "%d.%m.%Y %H:%M")),
                psychologist_id=timeslot.profile.id,
                user_id=user.id,
                meeting_id=meeting.id,
                meeting_format=MeetingFormat.ONLINE
                if meeting_format == buttons.BTN_MEETING_FORMAT_ONLINE.text
                else MeetingFormat.OFFLINE,
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


meeting_reschedule_section = ConversationHandler(
    entry_points=[
        make_message_handler(
            buttons.BTN_MEETING_RESCHEDULE, ask_for_reschedule(States.TYPING_MEETING_FORMAT)
        ),
    ],
    states={
        States.TYPING_MEETING_FORMAT: [
            make_message_handler(
                buttons.BTN_MEETING_FORMAT_ONLINE, ask_for_reschedule(States.TYPING_TIME_SLOT)
            ),
            make_message_handler(
                buttons.BTN_MEETING_FORMAT_OFFLINE, ask_for_reschedule(States.TYPING_TIME_SLOT)
            ),
        ],
        States.TYPING_TIME_SLOT: [
            make_text_handler(ask_for_reschedule(States.TYPING_MEETING_SLOT)),
        ],
        States.TYPING_MEETING_SLOT: [
            make_text_handler(ask_for_reschedule(States.TYPING_MEETING_CONFIRM))
        ],
        States.TYPING_MEETING_CONFIRM: [
            make_message_handler(buttons.BTN_CONFIRM_MEETING, meeting_update(True)),
            make_message_handler(buttons.BTN_NOT_CONFIRM_MEETING, meeting_update(False)),
        ],
    },
    fallbacks=[
        # make_message_handler(BTN_START_MENU, back_to_start_menu),
    ],
    map_to_parent={
        BotState.STOPPING: BotState.END,
    },
)
