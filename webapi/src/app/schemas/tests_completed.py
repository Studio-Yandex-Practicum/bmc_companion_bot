from datetime import datetime
from typing import List, Optional

from app.schemas.core import ObjectList
from pydantic import BaseModel


class TestCompletedCreate(BaseModel):
    """Схема создания результата пройденного теста."""

    user_id: int
    test_id: int
    value: int


class TestCompletedUpdate(TestCompletedCreate):
    """Схема обновления результата пройденного теста."""

    pass


class TestCompletedBare(BaseModel):
    """Схема получения краткой информации о результате теста."""

    user_id: int
    test_id: int
    value: int

    class Config:
        orm_mode = True


class TestCompletedFull(TestCompletedBare):
    """Схема получения полной информации о результате теста."""

    id: int
    created_at: Optional[datetime]


class TestCompletedList(ObjectList):
    """Схема получения списка результатов теста."""

    data: List[TestCompletedBare]
