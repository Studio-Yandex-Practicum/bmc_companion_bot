from datetime import datetime
from typing import List, Optional

from app.schemas.core import ObjectList
from pydantic import BaseModel, Extra, PositiveInt


class UserCreate(BaseModel):
    """Схема создания пользователя."""

    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    birthday: Optional[datetime]
    phone: Optional[PositiveInt]
    role_id: int
    telegram_id: Optional[PositiveInt]
    telegram_login: str | None

    class Config:
        min_anystr_length = 1
        extra = Extra.forbid


class UserUpdate(UserCreate):
    """Схема обновления пользователя."""

    pass


class UserBare(UserCreate):
    """Схема для получения краткой информации о пользователе."""

    id: int

    class Config:
        orm_mode = True


class UserFull(UserBare):
    """Схема для получения полной информации о пользователе."""

    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]


class UserList(ObjectList):
    """Схема для получения списка пользователей."""

    data: List[UserBare]
