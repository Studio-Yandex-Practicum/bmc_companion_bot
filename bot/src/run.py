import logging

from core.settings import settings
from handlers import admin, start
from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)
from ui import admin_button, admin_menu, homme_button, main_menu

updater = Updater(token=settings.BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def echo(update: Update, context: CallbackContext):
    if update.message.text == homme_button.text:
        main_menu(update, context)
    elif update.message.text == admin_button.text:
        admin_menu(update, context)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

admin_handler = CommandHandler("admin", admin)
dispatcher.add_handler(admin_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

if __name__ == "__main__":
    updater.start_polling()
