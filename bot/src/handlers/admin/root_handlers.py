from core.constants import BotState
from handlers.root_handlers import start
from request.clients import user_service
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from ui.buttons import (
    BTN_ADMINS_LIST,
    BTN_PSYCHOLOGISTS_LIST,
    BTN_START_MENU,
    BTN_TESTS_MENU,
)


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if user_service.is_staff(telegramm_id=update.message.chat.id):
        text = "Это админка!\nВыберите нужный раздел"
        buttons = [
            [BTN_ADMINS_LIST, BTN_PSYCHOLOGISTS_LIST, BTN_TESTS_MENU],
            [BTN_START_MENU],
        ]
        keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
        await update.message.reply_text(text, reply_markup=keyboard)
        return BotState.MENU_ADMIN_SELECTING_LEVEL
    else:
        await update.message.reply_text(text="Недостаточно прав для выполнения команды.")
        await back_to_start_menu(update, context)


async def back_to_start_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await start(update, context)
    return BotState.END


async def back_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await admin(update, context)
    return BotState.STOPPING
