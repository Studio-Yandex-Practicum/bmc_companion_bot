from core.constants import BotState
from handlers.admin.root_handlers import back_to_admin
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from ui.buttons import BTN_ADD_ADMIN, BTN_ADMIN_MENU, BTN_ADMINS_LIST, BTN_SHOW_ADMINS
from utils import make_message_handler

MENU_ADMINS_SELECTING_LEVEL = "MENU_ADMINS_SELECTING_LEVEL"


async def menu_admins_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    text = "Раздел редактирования админов"
    buttons = [
        [BTN_SHOW_ADMINS, BTN_ADD_ADMIN],
        [BTN_ADMIN_MENU],
    ]
    keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)

    await update.message.reply_text(text, reply_markup=keyboard)

    return MENU_ADMINS_SELECTING_LEVEL


admins_list_section = ConversationHandler(
    entry_points=[
        make_message_handler(BTN_ADMINS_LIST, menu_admins_list),
    ],
    states={
        MENU_ADMINS_SELECTING_LEVEL: [],
    },
    fallbacks=[
        make_message_handler(BTN_ADMIN_MENU, back_to_admin),
    ],
    map_to_parent={
        BotState.STOPPING: BotState.MENU_ADMIN_SELECTING_LEVEL,
    },
)
