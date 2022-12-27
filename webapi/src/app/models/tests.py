from app.models import BaseModel
from sqlalchemy import Column, DateTime, String, Text


class QuestionType(BaseModel):
    """Тип вопроса."""

    __tablename__ = "question_types"

    name = Column(String(256), comment="Название типа вопроса")
    validation_regexp = Column(
        Text, comment="Возможная валидация ответа на вопрос с помощью regexp"
    )
    deleted_at = Column(DateTime, comment="Время удаления")
