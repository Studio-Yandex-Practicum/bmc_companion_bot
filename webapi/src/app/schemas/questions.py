from datetime import datetime
from typing import List, Optional, Union

from app.schemas.core import ObjectList
from pydantic import BaseModel, Extra, Field


class QuestionTypeCreate(BaseModel):
    """Схема создания типа вопроса."""

    name: str = Field(..., max_length=256)
    validation_regexp: Optional[str]

    class Config:
        extra = Extra.forbid


class QuestionTypeUpdate(BaseModel):
    """Схема обновления типа вопроса."""

    name: Optional[str] = Field(None, max_length=256)
    validation_regexp: Optional[str]


class QuestionTypeResponse(QuestionTypeCreate):
    """Схема для получения полной информации о типе вопроса."""

    id: int
    name: Union[str, None]
    validation_regexp: Union[str, None]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True


class QuestionTypeList(ObjectList):
    """Схема для получения списка типов вопросов."""

    data: List[QuestionTypeResponse]
