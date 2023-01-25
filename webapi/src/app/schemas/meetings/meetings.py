from datetime import datetime

from app.schemas.core import ObjectList
from pydantic import BaseModel, Extra


class MeetingCreate(BaseModel):
    """Схема создания встречи."""

    client_id: int
    user_id: int
    type_id: int
    comment: None | str = None
    target_test_score: int
    time_slot: datetime

    class Config:
        extra = Extra.forbid


class MeetingUpdate(MeetingCreate):
    """Схема обновления встречи."""

    ...


class MeetingResponse(MeetingCreate):
    """Схема получения полной информации о встречи."""

    id: int
    created_at: datetime
    updated_at: None | datetime
    deleted_at: None | datetime

    class Config:
        orm_mode = True


class MeetingList(ObjectList):
    """Схема для получения списка встреч."""

    data: list[MeetingResponse]
