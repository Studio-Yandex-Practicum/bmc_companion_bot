import secrets
from typing import Callable

from core.constants import (
    DO_NOTHING_SIGN,
    KEY_RESULTS_FOR_PAGINATED_RESPONSE,
    RANDOM_STRING_CHARS,
)
from telegram import KeyboardButton
from telegram.ext import MessageHandler, filters


def make_random_password(length=10, allowed_chars=RANDOM_STRING_CHARS):
    return "".join(secrets.choice(allowed_chars) for _ in range(length))


def make_text_handler(callback: Callable):
    return MessageHandler(filters.TEXT, callback)


def make_message_handler(btn: KeyboardButton, callback: Callable):
    return MessageHandler(filters.Regex(f"^{btn.text}$"), callback)


def make_ask_for_input_information(main_text: str, value) -> str:
    text = main_text
    if value:
        text += f" (или введите {DO_NOTHING_SIGN}, чтобы оставить {value})"
    return f"{text}:"


def is_paginated_object(data: dict) -> bool:
    return KEY_RESULTS_FOR_PAGINATED_RESPONSE in data.keys()
