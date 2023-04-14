from enum import Enum
from typing import Any

from schemas.responses import FeedbackResponse, MeetingResponse, UserResponse
from telegram import ReplyKeyboardMarkup
from telegram.ext import ContextTypes


class ContextKeys(str, Enum):
    ANSWERS = "answers"
    BETTER_SCORE = "BETTER_SCORE"
    COMFORT_SCORE = "COMFORT_SCORE"
    COMMENT = "COMMENT"
    FEEDBACK = "FEEDBACK"
    FEEDBACK_TEXT = "FEEDBACK_TEXT"
    KEYBOARD = "current_keyboard"
    MEETING = "MEETING"
    MEETINGS = "meetings"
    MEETING_FORMAT = "MEETING_FORMAT"
    MEETING_NUMBER = "MEETING_NUMBER"
    TESTS = "tests"
    TIMESLOT = "TIMESLOT"
    TIMESLOTS = "TIMESLOTS"
    TIMESLOT_NUMBER = "TIMESLOT_NUMBER"
    PHONE = "phone"
    TEST_ID = "current_test_id"
    QUESTION_ID = "current_question_id"
    USER = "USER"
    USER_ID = "current_user_id"


class ContextManager:
    @staticmethod
    def set(context: ContextTypes.DEFAULT_TYPE, key: ContextKeys, value: Any) -> None:
        context.user_data[key] = value

    @staticmethod
    def get(context: ContextTypes.DEFAULT_TYPE, key: ContextKeys) -> Any:
        return context.user_data.get(key, None)

    def set_keys(self, context: ContextTypes.DEFAULT_TYPE, keys: ReplyKeyboardMarkup) -> None:
        self.set(context, ContextKeys.KEYBOARD, keys)

    def get_keys(self, context: ContextTypes.DEFAULT_TYPE) -> ReplyKeyboardMarkup:
        return self.get(context, ContextKeys.KEYBOARD)

    def set_tests(self, context: ContextTypes.DEFAULT_TYPE, tests: dict[str, int]) -> None:
        self.set(context, ContextKeys.TESTS, tests)

    def get_tests(self, context: ContextTypes.DEFAULT_TYPE) -> dict[str, int]:
        return self.get(context, ContextKeys.TESTS)

    def set_answers(self, context: ContextTypes.DEFAULT_TYPE, answers: dict[str, int]) -> None:
        self.set(context, ContextKeys.ANSWERS, answers)

    def get_answers(self, context: ContextTypes.DEFAULT_TYPE) -> dict[str, int]:
        return self.get(context, ContextKeys.ANSWERS)

    def set_user_phone(self, context: ContextTypes.DEFAULT_TYPE, phone: str) -> None:
        self.set(context, ContextKeys.PHONE, phone)

    def set_test_id(self, context: ContextTypes.DEFAULT_TYPE, test_id: int) -> None:
        self.set(context, ContextKeys.TEST_ID, test_id)

    def get_test_id(self, context: ContextTypes.DEFAULT_TYPE) -> int:
        return self.get(context, ContextKeys.TEST_ID)

    def set_question_id(self, context: ContextTypes.DEFAULT_TYPE, question_id: int):
        self.set(context, ContextKeys.QUESTION_ID, question_id)

    def get_question_id(self, context: ContextTypes.DEFAULT_TYPE) -> int:
        return self.get(context, ContextKeys.QUESTION_ID)

    def set_meetings(self, context: ContextTypes.DEFAULT_TYPE, meetings: list[MeetingResponse]):
        self.set(context, ContextKeys.MEETINGS, meetings)

    def get_meetings(self, context: ContextTypes.DEFAULT_TYPE) -> list[MeetingResponse]:
        return self.get(context, ContextKeys.MEETINGS)

    def set_user(self, context: ContextTypes.DEFAULT_TYPE, user: UserResponse):
        self.set(context, ContextKeys.USER, user)

    def get_user(self, context: ContextTypes.DEFAULT_TYPE) -> UserResponse:
        return self.get(context, ContextKeys.USER)

    def set_user_id(self, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> None:
        self.set(context, ContextKeys.USER_ID, user_id)

    def get_user_id(self, context: ContextTypes.DEFAULT_TYPE) -> int:
        return self.get(context, ContextKeys.USER_ID)

    def set_meeting_format(self, context: ContextTypes.DEFAULT_TYPE, meeting_format: str):
        self.set(context, ContextKeys.MEETING_FORMAT, meeting_format)

    def get_meeting_format(self, context: ContextTypes.DEFAULT_TYPE):
        return self.get(context, ContextKeys.MEETING_FORMAT)

    def set_meeting_number(self, context: ContextTypes.DEFAULT_TYPE, meeting_number: int):
        return self.set(context, ContextKeys.MEETING_NUMBER, meeting_number)

    def get_meeting_number(self, context: ContextTypes.DEFAULT_TYPE):
        return self.get(context, ContextKeys.MEETING_NUMBER)

    def set_meeting_comment(self, context: ContextTypes.DEFAULT_TYPE, comment: str):
        self.set(context, ContextKeys.COMMENT, comment)

    def get_meeting_comment(self, context: ContextTypes.DEFAULT_TYPE):
        return self.get(context, ContextKeys.COMMENT)

    def set_timeslots(self, context: ContextTypes.DEFAULT_TYPE, timeslots: list):
        self.set(context, ContextKeys.TIMESLOTS, timeslots)

    def get_timeslots(self, context: ContextTypes.DEFAULT_TYPE):
        return self.get(context, ContextKeys.TIMESLOTS)

    def set_timeslot(self, context: ContextTypes.DEFAULT_TYPE, timeslot: dict):
        self.set(context, ContextKeys.TIMESLOT, timeslot)

    def get_timeslot(self, context: ContextTypes.DEFAULT_TYPE):
        return self.get(context, ContextKeys.TIMESLOT)

    def set_timeslot_number(self, context: ContextTypes.DEFAULT_TYPE, timeslot_number: int):
        return self.set(context, ContextKeys.TIMESLOT_NUMBER, timeslot_number)

    def get_timeslot_number(self, context: ContextTypes.DEFAULT_TYPE):
        return self.get(context, ContextKeys.TIMESLOT_NUMBER)

    def set_meeting(self, context: ContextTypes.DEFAULT_TYPE, meeting: MeetingResponse):
        self.set(context, ContextKeys.MEETING, meeting)

    def get_meeting(self, context: ContextTypes.DEFAULT_TYPE):
        return self.get(context, ContextKeys.MEETING)

    def set_feedback(self, context: ContextTypes.DEFAULT_TYPE, feedback: FeedbackResponse):
        self.set(context, ContextKeys.FEEDBACK, feedback)

    def get_feedback(self, context: ContextTypes.DEFAULT_TYPE):
        return self.get(context, ContextKeys.FEEDBACK)

    def set_feedback_text(self, context: ContextTypes.DEFAULT_TYPE, feedback_text: str):
        self.set(context, ContextKeys.FEEDBACK_TEXT, feedback_text)

    def get_feedback_text(self, context: ContextTypes.DEFAULT_TYPE):
        return self.get(context, ContextKeys.FEEDBACK_TEXT)

    def set_comfort_score(self, context: ContextTypes.DEFAULT_TYPE, score: int):
        self.set(context, ContextKeys.COMFORT_SCORE, score)

    def set_better_score(self, context: ContextTypes.DEFAULT_TYPE, score: int):
        self.set(context, ContextKeys.BETTER_SCORE, score)

    def get_comfort_score(self, context: ContextTypes.DEFAULT_TYPE):
        return self.get(context, ContextKeys.COMFORT_SCORE)

    def get_better_score(self, context: ContextTypes.DEFAULT_TYPE):
        return self.get(context, ContextKeys.BETTER_SCORE)


context_manager = ContextManager()
