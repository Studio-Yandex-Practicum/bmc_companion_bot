from core.constants import BotState
from handlers.root_handlers import start
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from ui.buttons import (
    BTN_MEETING_CANCEL,
    BTN_MEETING_FIRST,
    BTN_MEETING_REPEAT,
    BTN_START_MENU,
)


async def meetings_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = "Выберите, что нужно сделать:"
    buttons = [
        [BTN_MEETING_FIRST, BTN_MEETING_REPEAT, BTN_MEETING_CANCEL],
        [BTN_START_MENU],
    ]
    keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    await update.message.reply_text(text, reply_markup=keyboard)
    return BotState.MENU_MEETING_SELECTING_LEVEL


async def back_to_start_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await start(update, context)
    return BotState.END
