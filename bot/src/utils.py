import secrets
from dataclasses import dataclass
from enum import Enum
from typing import Callable

import requests
from core.constants import (
    DO_NOTHING_SIGN,
    KEY_RESULTS_FOR_PAGINATED_RESPONSE,
    RANDOM_STRING_CHARS,
)
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters


def get_random_string(length, allowed_chars=RANDOM_STRING_CHARS):
    return "".join(secrets.choice(allowed_chars) for i in range(length))


def make_random_password(
    length=10, allowed_chars="abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
):
    return get_random_string(length, allowed_chars)


@dataclass
class DemoApiClient:
    def post(self, cb: str, data=None):
        d = data or {}
        d["cb"] = cb
        r = requests.post("http://127.0.0.1:5001/api/v1/healthcheck/", json=d)
        return r

    def get_admins(self):
        r = self.post("get_admins")
        return r.json()

    def get_users(self):
        r = self.post("get_users")
        return r.json()

    def get_user_by_tg_login(self, tg_login):
        r = self.post("get_user_by_tg_login", {"tg_login": tg_login})
        return r.json()

    def create_user(self, user_params):
        r = self.post("create_user", {"user_params": user_params})
        return r.json()

    def delete_user_by_id(self, user_id):
        r = self.post("delete_user_by_id", {"user_id": user_id})
        return r.json()

    def get_timeslots(self, tg_login):
        r = self.post("get_timeslots", {"tg_login": tg_login})
        return r.json()

    def create_timeslot(self, tg_login, timeslot):
        r = self.post("create_timeslot", {"tg_login": tg_login, "timeslot": timeslot})
        return r.json()


demo_api_client = DemoApiClient()


class ContextKeys(str, Enum):
    TESTS = "tests"
    ANSWERS = "answers"
    KEYBOARD = "current_keyboard"
    USER_ID = "current_user_id"
    TEST_ID = "current_test_id"
    QUESTION_ID = "current_question_id"
    PHONE = "phone"
    USER = "user"


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
