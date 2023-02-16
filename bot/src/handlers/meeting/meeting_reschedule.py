from core.constants import BotState
from handlers.meeting.root_handlers import back_to_start_menu
from telegram.ext import ConversationHandler
from ui.buttons import BTN_START_MENU
from utils import make_message_handler, make_text_handler

from . import buttons
from .enums import States
from .meeting_first import ask_for_input, process_meeting_confirm

meeting_reschedule_section = ConversationHandler(
    entry_points=[
        make_message_handler(
            buttons.BTN_MEETING_RESCHEDULE, ask_for_input(States.TYPING_MEETING_FORMAT)
        ),
    ],
    states={
        States.TYPING_MEETING_FORMAT: [
            make_message_handler(
                buttons.BTN_MEETING_FORMAT_ONLINE, ask_for_input(States.TYPING_TIME_SLOT)
            ),
            make_message_handler(
                buttons.BTN_MEETING_FORMAT_OFFLINE, ask_for_input(States.TYPING_TIME_SLOT)
            ),
        ],
        States.TYPING_TIME_SLOT: [
            make_text_handler(ask_for_input(States.TYPING_MEETING_CONFIRM)),
        ],
        States.TYPING_MEETING_CONFIRM: [
            make_message_handler(buttons.BTN_CONFIRM_MEETING, process_meeting_confirm(True)),
            make_message_handler(buttons.BTN_NOT_CONFIRM_MEETING, process_meeting_confirm(False)),
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
