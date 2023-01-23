from core.constants import BotState
from handlers.admin.admins_list import admins_list_section
from handlers.admin.root_handlers import admin, back_to_start_menu
from handlers.admin.tests import tests_section
from handlers.admin.users_list import users_list_section
from telegram.ext import CommandHandler, ConversationHandler
from ui.buttons import BTN_START_MENU
from utils import make_message_handler

selection_handlers = [
    tests_section,
    users_list_section,
    admins_list_section,
]


admin_section = ConversationHandler(
    entry_points=[CommandHandler("admin", admin)],
    states={
        BotState.MENU_ADMIN_SELECTING_LEVEL: selection_handlers,
    },
    fallbacks=[
        make_message_handler(BTN_START_MENU, back_to_start_menu),
    ],
    map_to_parent={
        BotState.STOPPING: BotState.END,
        BotState.END: BotState.MENU_START_SELECTING_LEVEL,
    },
)
