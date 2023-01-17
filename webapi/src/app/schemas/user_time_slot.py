from datetime import datetime
from typing import List, Optional

from app.schemas.core import ObjectList
from pydantic import BaseModel, Extra


class UserTimeSlotCreate(BaseModel):
    """Схема создания временных слотов."""

    date_start: datetime
    date_end: datetime

    class Config:
        extra = Extra.forbid


class UserTimeSlotUpdate(BaseModel):
    """Схема обновления временных слотов."""

    date_start: Optional[datetime]
    date_end: Optional[datetime]


class UserTimeSlotResponse(UserTimeSlotCreate):
    """Схема для получения полной информации о временных слотах."""

    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True


class UserTimeSlotList(ObjectList):
    """Схема для получения списка временных слотов."""

    data: List[UserTimeSlotResponse]
