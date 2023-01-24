from enum import Enum
from typing import Callable

from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters


class ContextKeys(str, Enum):
    TESTS = "tests"
    ANSWERS = "answers"
    KEYBOARD = "current_keyboard"
    USER_ID = "current_user_id"
    TEST_ID = "current_test_id"
    QUESTION_ID = "current_question_id"


class ContextManager:
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


def make_text_handler(callback: Callable):
    return MessageHandler(filters.TEXT, callback)


def make_message_handler(btn: KeyboardButton, callback: Callable):
    return MessageHandler(filters.Regex(f"^{btn.text}$"), callback)
