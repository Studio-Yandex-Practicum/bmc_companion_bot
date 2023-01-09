from core.constants import MOCK_TESTS
from telegram import Update
from telegram.ext import CallbackContext
from ui import main_menu, test_menus


def start(update: Update, context: CallbackContext):
    main_menu(update, context)


def test_menu(update: Update, context: CallbackContext):
    tests = MOCK_TESTS
    test_menus(update, context, tests)


def process_test_handler(update: Update, context: CallbackContext):
    #  test = MOCK_TESTS[1]
    pass
