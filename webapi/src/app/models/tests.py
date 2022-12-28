from datetime import datetime

from app.models import BaseModel
from sqlalchemy import Column, DateTime, String, Text, Integer


class QuestionType(BaseModel):
    """Тип вопроса."""

    __tablename__ = "question_types"

    name = Column(String(256), comment="Название типа вопроса")
    validation_regexp = Column(
        Text, comment="Возможная валидация ответа на вопрос с помощью regexp"
    )
    deleted_at = Column(DateTime, comment="Время удаления")

    def to_dict(self):
        return dict(
            name=self.name,
            validation_regexp=self.validation_regexp,
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at,
        )

    def from_dict(self, data):
        for key, item in data.items():
            setattr(self, key, item)


class Test(BaseModel):
    """Тесты."""
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True)
    name = Column(String(256), comment="Название теста", nullable=False)
    # created_by = Column(Integer, ForeignKey='user.id')
    deleted_at = Column(DateTime, default=None)

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            # created_by=test.created_by,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at
        )

    def from_dict(self, data):
        for key, item in data.items():
            setattr(self, key, item)
