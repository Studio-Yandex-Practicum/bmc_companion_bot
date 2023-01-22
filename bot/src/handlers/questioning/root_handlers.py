from core.constants import APIVersion, BotState
from handlers.root_handlers import start
from request.clients import TestAPIClient
from schemas.requests import UserIdRequestFromTelegram, UserSpecificRequest
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from ui.buttons import BTN_START_MENU

api_client = TestAPIClient(APIVersion.V1)


async def questioning_section(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await update.message.reply_text("Это раздел тестирования.")
    user_id = api_client.user_id_from_chat_id(
        UserIdRequestFromTelegram(chat_id=update.message.chat.id)
    ).user_id
    test_statuses = api_client.all_test_statuses(UserSpecificRequest(user_id=user_id))
    context.user_data["current_user_id"] = user_id
    buttons = []
    context.chat_data["test_list"] = {}
    if test_statuses.active.__root__:
        text = "Вы уже начинали проходить тест. Рекомендуем закончить его прохождение:"
        test_list = test_statuses.active.__root__
    elif test_statuses.available.__root__:
        text = "Вы можете пройти один из следующих тестов: "
        test_list = test_statuses.available.__root__
    else:
        text = "Вы уже прошли все доступные тесты."
        test_list = []
    for test in test_list:
        buttons.append([KeyboardButton(text=test.name)])
        context.chat_data["test_list"][test.name] = test.test_id
    buttons.append([BTN_START_MENU])
    keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    context.chat_data["current_keyboard"] = keyboard
    await update.message.reply_text(text, reply_markup=keyboard)
    return BotState.MENU_TEST_SELECTING_LEVEL


async def back_to_start_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await start(update, context)
    return BotState.END
