from datetime import datetime

from app.schemas.core import ObjectList
from pydantic import BaseModel, Extra, Field


class MeetingTypeCreate(BaseModel):
    """Схема для создания типа встречи."""

    name: str = Field(..., max_length=256)

    class Config:
        extra = Extra.forbid


class MeetingTypeUpdate(BaseModel):
    """Схема обновления типа встречи."""

    name: str


class MeetingTypeResponse(MeetingTypeCreate):
    """Схема для получения полной информации о типе встречи."""

    id: int
    created_at: datetime
    updated_at: None | datetime

    class Config:
        orm_mode = True


class MeetingTypeList(ObjectList):
    """Схема для получения списка вопросов."""

    data: list[MeetingTypeResponse]
