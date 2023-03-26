from app import user_service_v1
from core.constants import APIVersion, BotState
from decorators import at
from handlers.root_handlers import start
from request.clients import TestAPIClient
from schemas.requests import UserSpecificRequest
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from ui.buttons import BTN_START_MENU
from utils import context_manager

api_client = TestAPIClient(APIVersion.V1.value)


@at
async def back_to_start_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await start(update, context)
    return BotState.END


@at
async def test_questioning_section(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await update.message.reply_text("Это раздел тестирования.")
    chat_data = update.message.chat
    telegram_login = chat_data.username
    user = user_service_v1.get_user(username=telegram_login)
    if user is None:
        user = user_service_v1.create_user(
            telegram_login=telegram_login, first_name=chat_data.first_name, chat_id=chat_data.id
        )
    user_id = user.id
    test_statuses = api_client.all_test_statuses(UserSpecificRequest(user_id=user_id))
    context_manager.set_user_id(context, user_id)
    if test_statuses.active.items:
        active_test_names = "\n".join([f" — {test.name}" for test in test_statuses.active.items])
        text = f"Рекомендуем закончить прохождение уже начатых тестов:\n {active_test_names}"
        await update.message.reply_text(text)
    test_list = [*test_statuses.active.items, *test_statuses.available.items]
    if test_list:
        text = "Вы можете пройти один из следующих тестов: "
    else:
        text = "Вы уже прошли все доступные тесты."
        await update.message.reply_text(text)
        await back_to_start_menu(update, context)
        return BotState.END
    buttons = []
    context_manager.set_tests(context, {})
    for test in test_list:
        buttons.append([KeyboardButton(text=test.name)])
        context_manager.get_tests(context)[test.name] = test.id
    buttons.append([BTN_START_MENU])
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    context_manager.set_keys(context, keyboard)
    await update.message.reply_text(text, reply_markup=keyboard)
    return BotState.MENU_TEST_SELECTING_LEVEL
