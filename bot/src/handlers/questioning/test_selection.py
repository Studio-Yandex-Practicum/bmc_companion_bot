from core.constants import BotState
from decorators import at
from handlers.questioning.questioning import next_question
from handlers.root_handlers import error_restart
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from ui.buttons import BTN_START_MENU
from utils import context_manager


@at
async def test_selector(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    selected_text = update.message.text
    tests = context_manager.get_tests(context)
    if not tests:
        error_restart()
    if selected_text not in context_manager.get_tests(context):
        await update.message.reply_text(
            "выберите тест из списка", reply_markup=context_manager.get_keys(context)
        )
        return BotState.MENU_START_SELECTING_LEVEL
    test_id = context_manager.get_tests(context)[selected_text]
    context_manager.set_test_id(context, test_id)
    await update.message.reply_text(f"Вы выбрали тест «{selected_text}». Приступим!")
    await next_question(update, context)
    return BotState.QUESTIONING


test_selection = MessageHandler(~filters.Text(BTN_START_MENU.text), test_selector)
