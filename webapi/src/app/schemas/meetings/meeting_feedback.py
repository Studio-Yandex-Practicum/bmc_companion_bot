from datetime import datetime

from app.schemas.core import ObjectList
from pydantic import BaseModel, Extra


class MeetingFeedbackCreate(BaseModel):
    """Схема создания отзыва о встрече."""

    meeting_id: int
    user_id: int
    text: None | str = None
    score: int

    class Config:
        extra = Extra.forbid


class MeetingFeedbackUpdate(MeetingFeedbackCreate):
    """Схема обновления отзыва."""

    ...


class MeetingFeedbackResponse(MeetingFeedbackCreate):
    """Схема получения полной информации о отзыве."""

    id: int
    created_at: datetime
    updated_at: None | datetime
    deleted_at: None | datetime

    class Config:
        orm_mode = True


class MeetingFeedbackList(ObjectList):
    """Схема для получения списка отзывов."""

    data: list[MeetingFeedbackResponse]
