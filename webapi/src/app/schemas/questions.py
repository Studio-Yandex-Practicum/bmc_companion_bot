from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Extra, Field


class QuestionTypeCreate(BaseModel):
    name: str = Field(..., max_length=256)
    validation_regexp: Optional[str]

    class Config:
        extra = Extra.forbid


class QuestionTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=256)
    validation_regexp: Optional[str]


class QuestionTypeResponse(QuestionTypeCreate):
    id: int
    name: Union[str, None]
    validation_regexp: Union[str, None]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True
