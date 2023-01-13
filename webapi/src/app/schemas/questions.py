from datetime import datetime
from typing import List, Optional, Union

from app.schemas.core import ObjectList
from pydantic import BaseModel, Extra, Field


class QuestionCreate(BaseModel):
    """Схема создания вопроса."""

    text: str
    question_type_id: int

    class Config:
        extra = Extra.forbid


class QuestionUpdate(BaseModel):
    """Схема обновления вопроса."""

    text: Optional[str]
    question_type_id: Optional[int]


class QuestionResponse(QuestionCreate):
    """Схема для получения полной информации о вопросе."""

    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True


class QuestionResponseMini(QuestionUpdate):
    """Схема для получения краткой информации о вопросе."""

    id: int

    class Config:
        orm_mode = True


class QuestionList(ObjectList):
    """Схема для получения списка вопросов."""

    data: List[QuestionResponse]


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
    questions: List[QuestionResponseMini]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True


class QuestionTypeResponseMini(QuestionTypeCreate):
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

    data: List[QuestionTypeResponseMini]
