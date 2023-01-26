from core.constants import BotState
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from ui.buttons import BTN_MAKE_MEETING, BTN_SELECT_TEST


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        f"Привет, {update.message.chat.first_name}! "
        f"Мы приветствуем Ваше решение разобраться в себе.\n"
        "В нашем проекте есть настоящие профессионалы, которые помогут Вам сделать это."
    )
    buttons = [[BTN_SELECT_TEST, BTN_MAKE_MEETING]]
    keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    await update.message.reply_text(text, reply_markup=keyboard)

    return BotState.MENU_START_SELECTING_LEVEL


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Это справка"
    await update.message.reply_text(text)

    return BotState.MENU_START_SELECTING_LEVEL


async def error_restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Непредвиденная ошибка! Пожалуйста, сообщите о ней разработчику."
    await update.message.reply_text(text)
    await start(update, context)

    return BotState.MENU_START_SELECTING_LEVEL
