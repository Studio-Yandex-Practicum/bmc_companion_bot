from datetime import datetime
from typing import List, Optional, Union

from app.utils import get_paginated_list
from pydantic import BaseModel, Extra, Field, PositiveInt


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


class GetMultiQueryParams(BaseModel):
    """Схема параметров запроса."""

    start: int = Field(1, description="Смещение выбоки объектов")
    limit: int = Field(10, le=100, description="Количество объектов на одной странице")
    count: int = Field(None, description="Общее количество объектов")
    previous: str = Field(None, description="Предыдущая страница")
    next: str = Field(None, description="Следующая страница")


class UserList(GetMultiQueryParams):
    """Схема для получения списка пользователей."""

    data: List[UserBare]

    def pagination(self, data, query):
        return get_paginated_list(data, "/api/v1/users", query)

    class Config:
        orm_mode = True
