from core.constants import BotState
from handlers.meeting.enums import States
from handlers.meeting.feedback import ask_for_feedback
from handlers.meeting.meeting_cancel import meeting_cancel_section
from handlers.meeting.meeting_first import meeting_first_section
from handlers.meeting.meeting_repeat import meeting_repeat_section
from handlers.meeting.meeting_reschedule import meeting_reschedule_section
from handlers.meeting.root_handlers import back_to_start_menu, meetings_main_menu
from telegram.ext import ConversationHandler
from ui.buttons import BTN_FEEDBACK, BTN_MAKE_MEETING, BTN_START_MENU
from utils import make_message_handler, make_text_handler

selection_handlers = [
    meeting_first_section,
    meeting_repeat_section,
    meeting_cancel_section,
    meeting_reschedule_section,
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

feedback_section = ConversationHandler(
    entry_points=[
        make_message_handler(BTN_FEEDBACK, ask_for_feedback(States.TYPING_MEETING_NUMBER)),
    ],
    states={
        States.TYPING_MEETING_NUMBER: [
            make_text_handler(ask_for_feedback(States.CHECK_IS_FEEDBACK_LEFT)),
        ],
        States.CHECK_IS_FEEDBACK_LEFT: [
            make_text_handler(ask_for_feedback(States.TYPING_COMFORT_SCORE)),
        ],
        States.TYPING_COMFORT_SCORE: [
            make_text_handler(ask_for_feedback(States.TYPING_BETTER_SCORE)),
        ],
        States.TYPING_BETTER_SCORE: [
            make_text_handler(ask_for_feedback(States.FEEDBACK_SAVED)),
        ],
    },
    fallbacks=[
        make_message_handler(BTN_START_MENU, back_to_start_menu),
    ],
    map_to_parent={
        BotState.END: BotState.MENU_START_SELECTING_LEVEL,
    },
)
