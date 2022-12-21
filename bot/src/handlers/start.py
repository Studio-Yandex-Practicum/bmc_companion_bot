from telegram import Update
from telegram.ext import CallbackContext
from ui import main_menu


def start(update: Update, context: CallbackContext):
    main_menu(update, context)
