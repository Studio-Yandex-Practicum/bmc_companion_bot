from datetime import datetime
from typing import List, TypeVar, Union

from pydantic import BaseModel, PositiveInt

ListElement = TypeVar("ListElement", bound=BaseModel)


class ObjectList(BaseModel):
    """Схема для получения списка элементов."""

    data: List[ListElement]

    class Config:
        orm_mode = True


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


class UserList(ObjectList):
    """Схема для получения списка пользователей."""

    data: List[UserBare]
