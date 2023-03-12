from app import schedule_service_v1, user_service_v1
from core.constants import BotState, MeetingFormat
from decorators import at
from handlers.meeting.root_handlers import back_to_start_menu
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from ui.buttons import BTN_START_MENU
from utils import context_manager, make_message_handler, make_text_handler

from . import buttons
from .enums import States
from .messages import psychologist_meeting_message


@at
async def get_meetings_list_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получить список записей встреч клиента."""
    chat_data_id = update.message.chat.id
    user = user_service_v1.get_user(chat_id=chat_data_id)
    context_manager.set_user(context, user)
    meetings = schedule_service_v1.get_meetings_by_user(user_id=user.id, is_active="True")
    text_parts = ["Запись для отмены:\n"]
    for index, meeting in enumerate(meetings):
        psychologist_profile = user_service_v1.get_user(id=meeting.psychologist)
        text_parts.append(f"\n{psychologist_profile.first_name} {psychologist_profile.last_name} ")
        text_parts.append(f"{meeting.date_start}")

    if not meetings:
        text_parts = ["У вас нет записи"]

    keys = [
        [buttons.BTN_MEETING_CANCEL],
        [BTN_START_MENU],
    ]
    keyboard = ReplyKeyboardMarkup(keys, one_time_keyboard=True)
    context_manager.set_keys(context, keyboard)
    context_manager.set_meetings(context, meetings)

    await update.message.reply_text(text="".join(text_parts), reply_markup=keyboard)

    return States.TYPING_MEETING_LIST


@at
async def meeting_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удаляет запись к психологу."""
    meeting_number = update.message.text
    meetings = context_manager.get_meetings(context)
    if meeting_number == "Отмена записи":
        schedule_service_v1.delete_meeting(meeting_id=meetings[0].id)
        text_parts = ["Запись отменена"]
    else:
        await back_to_start_menu(update, context)
        return BotState.STOPPING
    psychologist_id = meetings[0].psychologist
    if psychologist_id:
        meeting = meetings[0]
        user = context_manager.get_user(context)
        psychologist = user_service_v1.get_user(id=psychologist_id)
        meeting_format = "Онлайн" if meeting.format == MeetingFormat.ONLINE else "Очно"
        meeting_text = await psychologist_meeting_message(
            meeting_format, user, meeting, header="Ваша запись была отменена:\n"
        )
        await context.bot.send_message(chat_id=psychologist.chat_id, text=meeting_text)
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
        make_message_handler(BTN_START_MENU, back_to_start_menu),
    ],
    map_to_parent={
        BotState.STOPPING: BotState.END,
        BotState.END: BotState.MENU_MEETING_SELECTING_LEVEL,
    },
)
