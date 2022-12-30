from app.models import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class Question(BaseModel):
    """Модель вопроса."""

    __tablename__ = "questions"

    text = Column(Text)
    question_type_id = Column(Integer, ForeignKey("question_types.id"), nullable=False)
    deleted_at = Column(DateTime, comment="Время удаления")

    def to_dict(self):
        return dict(
            text=self.text,
            question_type_id=self.question_type_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at,
        )

    def from_dict(self, data):
        for key, item in data.items():
            setattr(self, key, item)


class QuestionType(BaseModel):
    """Тип вопроса."""

    __tablename__ = "question_types"

    name = Column(String(256), comment="Название типа вопроса")
    validation_regexp = Column(
        Text, comment="Возможная валидация ответа на вопрос с помощью regexp"
    )
    deleted_at = Column(DateTime, comment="Время удаления")
    questions = relationship("Question")

    def to_dict(self):
        return dict(
            name=self.name,
            validation_regexp=self.validation_regexp,
            questions=self.questions,
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
    created_by = Column(Integer, ForeignKey("users.id"))
    deleted_at = Column(DateTime, default=None)

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            # created_by=test.created_by,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at,
        )

    def from_dict(self, data):
        for key, item in data.items():
            setattr(self, key, item)
