from app.models import BaseModel
from sqlalchemy import Column, DateTime, String, Text


class QuestionType(BaseModel):
    __tablename__ = "question_types"

    name = Column("Тип вопроса", String(256))
    validation_regexp = Column("Валидация ответа", Text)
    deleted_at = Column("Время удаления", DateTime)

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
