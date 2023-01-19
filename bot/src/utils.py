from typing import Callable

from telegram import KeyboardButton
from telegram.ext import MessageHandler, filters


def make_text_handler(callback: Callable):
    return MessageHandler(filters.TEXT, callback)


def make_message_handler(btn: KeyboardButton, callback: Callable):
    return MessageHandler(filters.Regex(f"^{btn.text}$"), callback)
