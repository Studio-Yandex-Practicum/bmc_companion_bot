from app import user_service_v1
from core.constants import BotState
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from ui.buttons import BTN_FEEDBACK, BTN_MAKE_MEETING, BTN_SELECT_TEST


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_data = update.message.chat
    telegram_login = chat_data.username
    text = (
        f"Привет, {chat_data.first_name}! "
        f"Мы приветствуем Ваше решение разобраться в себе.\n"
        "В нашем проекте есть настоящие профессионалы, которые помогут Вам сделать это."
    )
    buttons = [[BTN_SELECT_TEST, BTN_MAKE_MEETING, BTN_FEEDBACK]]
    keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)

    user = user_service_v1.get_user(username=telegram_login)
    if user is None:
        user_service_v1.create_user(
            telegram_login=telegram_login, first_name=chat_data.first_name, chat_id=chat_data.id
        )

        await update.message.reply_text(text, reply_markup=keyboard)

    else:
        await update.message.reply_text("Вы в главном меню", reply_markup=keyboard)

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
