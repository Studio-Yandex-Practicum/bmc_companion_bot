from enum import Enum

from base import BaseContextManager
from schemas.responses import FeedbackResponse, MeetingResponse, UserResponse
from telegram.ext import ContextTypes


class ContextKeys(str, Enum):
    USER = "USER"
    COMMENT = "COMMENT"
    MEETING_FORMAT = "MEETING_FORMAT"
    TIMESLOTS = "TIMESLOTS"
    TIMESLOT = "TIMESLOT"
    MEETING = "MEETING"
    FEEDBACK = "FEEDBACK"
    FEEDBACK_TEXT = "FEEDBACK_TEXT"
    SCORE = "SCORE"


class MeetingContextManager(BaseContextManager):
    def set_user(self, context: ContextTypes.DEFAULT_TYPE, user: UserResponse):
        self.set(context, ContextKeys.USER, user)

    def get_user(self, context: ContextTypes.DEFAULT_TYPE):
        return self.get(context, ContextKeys.USER)

    def get_user_id(self, context: ContextTypes.DEFAULT_TYPE):
        user_id = None
        user = self.get_user(context)
        if user and isinstance(user, dict):
            user_id = user.get("id")
        return user_id

    def set_meeting_format(self, context: ContextTypes.DEFAULT_TYPE, meeting_format: str):
        self.set(context, ContextKeys.MEETING_FORMAT, meeting_format)

    def get_meeting_format(self, context: ContextTypes.DEFAULT_TYPE):
        return self.get(context, ContextKeys.MEETING_FORMAT)

    def set_meeting_comment(self, context: ContextTypes.DEFAULT_TYPE, comment: str):
        self.set(context, ContextKeys.COMMENT, comment)

    def get_comment(self, context: ContextTypes.DEFAULT_TYPE):
        return self.get(context, ContextKeys.COMMENT)

    def set_timeslots(self, context: ContextTypes.DEFAULT_TYPE, timeslots: list):
        self.set(context, ContextKeys.TIMESLOTS, timeslots)

    def get_timeslots(self, context: ContextTypes.DEFAULT_TYPE):
        return self.get(context, ContextKeys.TIMESLOTS)

    def set_timeslot(self, context: ContextTypes.DEFAULT_TYPE, timeslot: dict):
        self.set(context, ContextKeys.TIMESLOT, timeslot)

    def get_timeslot(self, context: ContextTypes.DEFAULT_TYPE):
        return self.get(context, ContextKeys.TIMESLOT)

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

    def set_score(self, context: ContextTypes.DEFAULT_TYPE, score: int):
        self.set(context, ContextKeys.SCORE, score)

    def get_score(self, context: ContextTypes.DEFAULT_TYPE):
        return self.get(context, ContextKeys.SCORE)


context_manager = MeetingContextManager()
