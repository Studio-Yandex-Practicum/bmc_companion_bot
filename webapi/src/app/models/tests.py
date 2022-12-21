from app.models import BaseModel
from sqlalchemy import Column, DateTime, String, Text


class QuestionType(BaseModel):
    __tablename__ = "question_types"

    name = Column("Тип вопроса", String(256))
    validation_regex = Column("Валидация ответа", Text)
    deleted_at = Column("Время удаления", DateTime)
