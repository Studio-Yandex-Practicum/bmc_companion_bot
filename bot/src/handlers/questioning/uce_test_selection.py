from app import questioning_service_v1, user_service_v1
from context_manager import context_manager
from core.constants import BotState
from decorators import at
from handlers.meeting.buttons import BTN_I_DONT_KNOW
from handlers.questioning.questioning import next_question, question_handler
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from utils import make_message_handler


@at
async def go_to_uce_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "выполняется переход на прохождение теста НДО:"
    chat_data = update.message.chat
    telegram_login = chat_data.username
    user = user_service_v1.get_user(username=telegram_login)
    if user is None:
        user = user_service_v1.create_user(
            telegram_login=telegram_login, first_name=chat_data.first_name, chat_id=chat_data.id
        )
    user_id = user.id
    context_manager.set_user_id(context, user_id)
    uce_test_id = questioning_service_v1.uce_test_id().id
    context_manager.set_test_id(context, uce_test_id)
    await update.message.reply_text(text)
    await next_question(update, context)
    return BotState.QUESTIONING


uce_test_section = ConversationHandler(
    entry_points=[make_message_handler(BTN_I_DONT_KNOW, go_to_uce_test)],
    states={
        BotState.QUESTIONING: [question_handler],
    },
    fallbacks=[
        # make_message_handler(BTN_START_MENU, back_to_start_menu),
    ],
    map_to_parent={
        BotState.STOPPING: BotState.END,
        BotState.END: BotState.MENU_START_SELECTING_LEVEL,
    },
)
