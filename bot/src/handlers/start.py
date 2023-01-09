from mock.tests import MOCK_TESTS
from telegram import Update
from telegram.ext import CallbackContext
from ui import main_menu


def start(update: Update, context: CallbackContext):
    context.bot_data["tests"] = MOCK_TESTS
    main_menu(update, context)
