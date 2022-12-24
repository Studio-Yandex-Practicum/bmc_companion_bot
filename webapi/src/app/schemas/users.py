from datetime import datetime
from typing import Optional, Union

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

    class Config:
        min_anystr_length = 1
        extra = Extra.forbid


class UserUpdate(UserCreate):
    """Схема обновления пользователя."""

    pass


class UserBare(BaseModel):
    """Схема для получения краткой информации о пользователе."""

    id: int
    first_name: Union[str, None]
    last_name: Union[str, None]
    middle_name: Union[str, None]
    birthday: Union[datetime, None]
    phone: Union[PositiveInt, None]
    role_id: int
    telegram_id: Union[PositiveInt, None]

    class Config:
        orm_mode = True


class UserFull(UserBare):
    """Схема для получения полной информации о пользователе."""

    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]


class UserList(UserBare):
    """Схема для получения списка пользователей."""

    pass
