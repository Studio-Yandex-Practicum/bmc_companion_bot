from core.constants import BotState
from handlers.questioning.questioning import question_handler
from handlers.questioning.root_handlers import (
    back_to_start_menu,
    test_questioning_section,
)
from handlers.questioning.test_selection import test_selection
from telegram.ext import ConversationHandler
from ui.buttons import BTN_SELECT_TEST, BTN_START_MENU
from utils import make_message_handler

questioning_section = ConversationHandler(
    entry_points=[
        make_message_handler(BTN_SELECT_TEST, test_questioning_section),
    ],
    states={
        BotState.MENU_TEST_SELECTING_LEVEL: [test_selection],
        BotState.QUESTIONING: [question_handler],
    },
    fallbacks=[
        make_message_handler(BTN_START_MENU, back_to_start_menu),
    ],
    map_to_parent={
        BotState.STOPPING: BotState.END,
        BotState.END: BotState.MENU_TEST_SELECTING_LEVEL,
        BotState.MENU_TEST_SELECTING_LEVEL: BotState.MENU_START_SELECTING_LEVEL,
    },
)
