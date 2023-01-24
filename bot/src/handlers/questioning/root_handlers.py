from core.constants import APIVersion, BotState
from handlers.root_handlers import start
from mock.mock_test_client import MockTestAPIClient as TestAPIClient
from schemas.requests import UserIdRequestFromTelegram, UserSpecificRequest
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from ui.buttons import BTN_START_MENU
from utils import context_manager

api_client = TestAPIClient(APIVersion.V1)


async def questioning_section(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await update.message.reply_text("Это раздел тестирования.")
    user_id = api_client.user_id_from_chat_id(
        UserIdRequestFromTelegram(chat_id=update.message.chat.id)
    ).user_id
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
    buttons = []
    context_manager.set_tests(context, {})
    for test in test_list:
        buttons.append([KeyboardButton(text=test.name)])
        context_manager.get_tests(context)[test.name] = test.test_id
    buttons.append([BTN_START_MENU])
    keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    context_manager.set_keys(context, keyboard)
    await update.message.reply_text(text, reply_markup=keyboard)
    return BotState.MENU_TEST_SELECTING_LEVEL


async def back_to_start_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await start(update, context)
    return BotState.END
