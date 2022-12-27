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
