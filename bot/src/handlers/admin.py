from telegram import Update
from telegram.ext import CallbackContext
from ui import admin_menu


def admin(update: Update, context: CallbackContext):
    admin_menu(update, context)
