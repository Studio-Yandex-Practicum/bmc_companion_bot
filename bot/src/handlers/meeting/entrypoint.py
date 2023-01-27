from core.constants import BotState
from handlers.meeting.meeting_first import meeting_first_section
from handlers.meeting.root_handlers import back_to_start_menu, meetings_main_menu
from telegram.ext import ConversationHandler
from ui.buttons import BTN_MAKE_MEETING, BTN_START_MENU
from utils import make_message_handler

selection_handlers = [
    meeting_first_section,
    # users_list_section,
    # admins_list_section,
]


meeting_section = ConversationHandler(
    entry_points=[
        make_message_handler(BTN_MAKE_MEETING, meetings_main_menu),
    ],
    states={
        BotState.MENU_MEETING_SELECTING_LEVEL: selection_handlers,
    },
    fallbacks=[
        make_message_handler(BTN_START_MENU, back_to_start_menu),
    ],
    map_to_parent={
        BotState.END: BotState.MENU_START_SELECTING_LEVEL,
    },
)
