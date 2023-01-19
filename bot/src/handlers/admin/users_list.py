from core.constants import BotState
from handlers.admin.root_handlers import back_to_admin
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from ui.buttons import (
    BTN_ADD_USER,
    BTN_ADMIN_MENU,
    BTN_PSYCHOLOGISTS_LIST,
    BTN_SHOW_USERS,
)
from utils import make_message_handler

MENU_USERS_SELECTING_LEVEL = "MENU_USERS_SELECTING_LEVEL"


async def main_users_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    text = "Раздел редактирования психологов"
    buttons = [
        [BTN_SHOW_USERS, BTN_ADD_USER],
        [BTN_ADMIN_MENU],
    ]
    keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)

    await update.message.reply_text(text, reply_markup=keyboard)

    return MENU_USERS_SELECTING_LEVEL


users_list_section = ConversationHandler(
    entry_points=[
        make_message_handler(BTN_PSYCHOLOGISTS_LIST, main_users_list),
    ],
    states={
        MENU_USERS_SELECTING_LEVEL: [],
    },
    fallbacks=[
        make_message_handler(BTN_ADMIN_MENU, back_to_admin),
    ],
    map_to_parent={
        BotState.STOPPING: BotState.MENU_ADMIN_SELECTING_LEVEL,
    },
)
