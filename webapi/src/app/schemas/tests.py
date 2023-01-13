from datetime import datetime
from typing import List, Optional

from app.schemas.core import ObjectList
from pydantic import BaseModel, Extra


class TestCreate(BaseModel):
    name: str
    created_by: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True


class TestResponse(TestCreate):
    id: int
    created_at: datetime
    created_by: int

    class Config:
        orm_mode = True


class TestList(ObjectList):
    data: List[TestResponse]


class TestProgressUpdate(BaseModel):
    """Схема для обновления прогресса."""

    test_question_id: int

    class Config:
        extra = Extra.forbid


class TestProgressCreate(TestProgressUpdate):
    """Схема для создания прогресса."""

    user_id: int


class TestProgressBare(TestProgressCreate):
    """Схема для получения краткой информации о прогрессе."""

    id: int

    class Config:
        orm_mode = True


class TestProgressFull(TestProgressBare):
    """Схема для получения полной информации о прогрессе."""

    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]


class TestProgressList(ObjectList):
    """Схема для получения списка пользователей."""

    data: List[TestProgressBare]


class TestCompletedUpdate(BaseModel):
    """Схема для обновления данных завершенных тестов."""

    value: int

    class Config:
        extra = Extra.forbid


class TestCompletedCreate(TestCompletedUpdate):
    """Схема для завершение теста."""

    user_id: int
    test_id: int


class TestCompletedBare(TestCompletedCreate):
    """Схема для получения краткой информации о завершенных тестах."""

    id: int

    class Config:
        orm_mode = True


class TestCompletedFull(TestCompletedBare):
    """Схема для получения полной информации о завершенных тестах."""

    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]


class TestCompletedList(ObjectList):
    """Схема для получения списка пользователей."""

    data: List[TestCompletedBare]
