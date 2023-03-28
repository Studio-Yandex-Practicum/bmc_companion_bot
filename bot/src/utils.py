import secrets
from enum import Enum
from typing import Callable

from core.constants import (
    DO_NOTHING_SIGN,
    KEY_RESULTS_FOR_PAGINATED_RESPONSE,
    RANDOM_STRING_CHARS,
)
from schemas.responses import MeetingResponse
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters


def make_random_password(length=10, allowed_chars=RANDOM_STRING_CHARS):
    return "".join(secrets.choice(allowed_chars) for i in range(length))


class ContextKeys(str, Enum):
    TESTS = "tests"
    ANSWERS = "answers"
    KEYBOARD = "current_keyboard"
    USER_ID = "current_user_id"
    TEST_ID = "current_test_id"
    QUESTION_ID = "current_question_id"
    PHONE = "phone"
    USER = "user"
    MEETINGS = "meetings"


class ContextManager:
    def set(self, context: ContextTypes.DEFAULT_TYPE, key, value):
        context.user_data[key] = value

    def get(self, context: ContextTypes.DEFAULT_TYPE, key):
        return context.user_data.get(key)

    def set_keys(self, context: ContextTypes.DEFAULT_TYPE, keys: ReplyKeyboardMarkup):
        context.chat_data[ContextKeys.KEYBOARD] = keys

    def get_keys(self, context: ContextTypes.DEFAULT_TYPE) -> ReplyKeyboardMarkup:
        return context.chat_data.get(ContextKeys.KEYBOARD)

    def set_tests(self, context: ContextTypes.DEFAULT_TYPE, tests: dict[str, int]):
        context.chat_data[ContextKeys.TESTS] = tests

    def get_tests(self, context: ContextTypes.DEFAULT_TYPE) -> dict[str, int]:
        return context.chat_data.get(ContextKeys.TESTS)

    def set_answers(self, context: ContextTypes.DEFAULT_TYPE, answers: dict[str, int]):
        context.chat_data[ContextKeys.ANSWERS] = answers

    def get_answers(self, context: ContextTypes.DEFAULT_TYPE) -> dict[str, int]:
        return context.chat_data.get(ContextKeys.ANSWERS)

    def set_user_id(self, context: ContextTypes.DEFAULT_TYPE, user_id: int):
        context.user_data[ContextKeys.USER_ID] = user_id

    def set_user_phone(self, context: ContextTypes.DEFAULT_TYPE, phone: str):
        context.user_data[ContextKeys.PHONE] = phone

    def set_user(self, context: ContextTypes.DEFAULT_TYPE, user):
        context.user_data[ContextKeys.USER] = user

    def get_user(self, context: ContextTypes.DEFAULT_TYPE):
        return context.user_data.get(ContextKeys.USER)

    def get_user_id(self, context: ContextTypes.DEFAULT_TYPE) -> int:
        return context.user_data.get(ContextKeys.USER_ID)

    def set_test_id(self, context: ContextTypes.DEFAULT_TYPE, test_id: int):
        context.user_data[ContextKeys.TEST_ID] = test_id

    def get_test_id(self, context: ContextTypes.DEFAULT_TYPE) -> int:
        return context.user_data.get(ContextKeys.TEST_ID)

    def set_question_id(self, context: ContextTypes.DEFAULT_TYPE, question_id: int):
        context.user_data[ContextKeys.QUESTION_ID] = question_id

    def get_question_id(self, context: ContextTypes.DEFAULT_TYPE) -> int:
        return context.user_data.get(ContextKeys.QUESTION_ID)

    def set_meetings(self, context: ContextTypes.DEFAULT_TYPE, meetings: list[MeetingResponse]):
        context.chat_data[ContextKeys.MEETINGS] = meetings

    def get_meetings(self, context: ContextTypes.DEFAULT_TYPE) -> list[MeetingResponse]:
        return context.chat_data.get(ContextKeys.MEETINGS)


context_manager = ContextManager()


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
