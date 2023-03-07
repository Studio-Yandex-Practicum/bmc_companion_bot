from app import schedule_service_v1, user_service_v1
from core.constants import BotState
from handlers.meeting.root_handlers import back_to_start_menu
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from ui.buttons import BTN_START_MENU
from utils import context_manager, make_message_handler, make_text_handler

from . import buttons
from .enums import States


async def get_meetings_list_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получить список записей встреч клиента."""
    chat_data_id = update.message.chat.id
    user = user_service_v1.get_user(chat_id=chat_data_id)
    meetings = schedule_service_v1.get_meetings_by_user(chat_id=user.chat_id)

    text_parts = ["Выберите запись для отмены:\n"]
    for index, meeting in enumerate(meetings, start=1):
        psychologist_profile = user_service_v1.get_user(id=meeting.psychologist)
        text_parts.append(
            f"\n{index}. {psychologist_profile.first_name} {psychologist_profile.last_name} "
        )
        text_parts.append(f"{meeting.date_start}")

    if not meetings:
        text_parts = ["У вас нет записи"]

    buttons = [[BTN_START_MENU]]
    keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    context_manager.set_keys(context, keyboard)
    context_manager.set_meetings(context, meetings)

    await update.message.reply_text(text="".join(text_parts), reply_markup=keyboard)

    return States.TYPING_MEETING_LIST


async def meeting_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удаляет запись к психологу."""
    meeting_number = update.message.text
    meetings = context_manager.get_meetings(context)
    count_of_meetings = len(meetings)
    if meeting_number == "Главное меню":
        await back_to_start_menu(update, context)
        return BotState.STOPPING
    if str(meeting_number).isnumeric():
        if int(meeting_number) <= count_of_meetings:
            meeting_id = meetings[int(meeting_number) - 1].id
            schedule_service_v1.delete_meeting(meeting_id=meeting_id)
            text_parts = ["Запись отменена"]
        else:
            text_parts = ["Укажите верный номер записи"]

    else:
        text_parts = ["Введите цифру записи"]

    buttons = [[BTN_START_MENU]]
    keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)

    await update.message.reply_text(text="".join(text_parts), reply_markup=keyboard)

    await back_to_start_menu(update, context)

    return BotState.STOPPING


meeting_cancel_section = ConversationHandler(
    entry_points=[
        make_message_handler(buttons.BTN_MEETING_CANCEL, get_meetings_list_user),
    ],
    states={
        States.TYPING_MEETING_LIST: [
            make_text_handler(meeting_cancel),
        ],
    },
    fallbacks=[
        # make_message_handler(BTN_START_MENU, back_to_start_menu),
    ],
    map_to_parent={
        BotState.STOPPING: BotState.END,
    },
)
