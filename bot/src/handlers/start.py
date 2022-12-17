from handlers import constants as const
from telegram import Message, Update
from telegram.ext import CallbackContext


def start(update: Update, context: CallbackContext) -> Message:
    context.bot.send_message(chat_id=update.effective_chat.id, text=const.GREETING_MESSAGE)
