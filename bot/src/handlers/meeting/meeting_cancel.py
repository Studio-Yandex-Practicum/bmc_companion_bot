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
    """Получить список записей встречь клиента."""
    text = ""
    chat_data = update.message.chat
    user = user_service_v1.get_user(chat_id=chat_data.id)
    meetings = schedule_service_v1.get_meetings_by_user(chat_id=user.chat_id)

    if not meetings:
        text = "У вас нет записи"

    for index, meeting in enumerate(meetings):
        text = "Выберите запись для отмены:\n"
        psychologist_profile = user_service_v1.get_user(id=meeting.psychologist)
        text += f"\n{index+1}. {psychologist_profile.first_name} {psychologist_profile.last_name} "
        text += f"{meeting.date_start}"

    buttons = [[BTN_START_MENU]]
    keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    context_manager.set_keys(context, keyboard)
    context_manager.set_meetings(context, meetings)

    await update.message.reply_text(text=text, reply_markup=keyboard)

    return States.TYPING_MEETING_LIST


async def meeting_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удаляет запись к психологу."""
    await update.message.reply_text("Запись отменена")
    meeting_number = int(update.message.text)
    meetings = context_manager.get_meetings(context)
    meeting_id = meetings[meeting_number - 1].id
    schedule_service_v1.delete_meeting(meeting_id=meeting_id)


meeting_cancel_section = ConversationHandler(
    entry_points=[
        make_message_handler(buttons.BTN_MEETING_CANCEL, get_meetings_list_user),
    ],
    states={
        States.TYPING_MEETING_LIST: [
            make_message_handler(BTN_START_MENU, back_to_start_menu),
            make_text_handler(meeting_cancel),
        ],
    },
    fallbacks=[
        make_message_handler(BTN_START_MENU, back_to_start_menu),
    ],
    map_to_parent={
        BotState.STOPPING: BotState.END,
        BotState.END: BotState.MENU_START_SELECTING_LEVEL,
    },
)
