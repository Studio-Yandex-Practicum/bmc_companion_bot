from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext

from . import constants as const


def main_menu(update: Update, context: CallbackContext):
    buttons = ReplyKeyboardMarkup([["Тесты"], ["Запись к психологу"]], resize_keyboard=True)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=const.GREETING_MESSAGE, reply_markup=buttons
    )
