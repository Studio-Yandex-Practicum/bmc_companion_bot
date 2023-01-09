from typing import Dict, List

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext
from ui import MenuNames


def main_menu(update: Update, context: CallbackContext) -> None:
    buttons = ReplyKeyboardMarkup(
        [[MenuNames.start_menu("to_test")], [MenuNames.start_menu("to_meeting")]],
        resize_keyboard=True,
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MenuNames.start_menu.result.format(update.message.chat.first_name),
        reply_markup=buttons,
    )


def test_menus(update: Update, context: CallbackContext, tests: List) -> None:
    buttons_layout = [[test["name"]] for test in tests]
    buttons = ReplyKeyboardMarkup(
        buttons_layout,
        resize_keyboard=True,
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MenuNames.test_menus.result,
        reply_markup=buttons,
    )


def process_question(update: Update, context: CallbackContext, question: Dict) -> None:
    buttons_layout = [[answer["text"] for answer in question["answers"]]]
    buttons = ReplyKeyboardMarkup(
        buttons_layout,
        resize_keyboard=True,
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MenuNames.test_menus.result,
        reply_markup=buttons,
    )


def process_test(update: Update, context: CallbackContext, test: Dict) -> None:
    for question in test["questions"]:
        process_question(update, context, question)
