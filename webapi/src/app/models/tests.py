from datetime import datetime

from app import db
from sqlalchemy import Column, DateTime, Integer, String, Text


def current_time() -> datetime:
    return datetime.utcnow


class QuestionType(db.Model):
    __tablename__ = "question_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column("Тип вопроса", String(256))
    validation_regex = Column("Валидация ответа", Text)
    created_at = Column("Время создания", DateTime, default=current_time)
    updated_at = Column("Время обновления", DateTime, onupdate=current_time)
    deleted_at = Column("Время удаления", DateTime)
