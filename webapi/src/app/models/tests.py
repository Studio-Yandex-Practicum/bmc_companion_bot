from app.models import BaseModel
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
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


class TestProgress(BaseModel):
    """Модель прогресса прохождения теста пользователем."""

    __tablename__ = "tests_progress"
    __table_args__ = (UniqueConstraint("user_id", "test_question_id", name="unique_progress"),)

    test_question_id = Column(Integer, ForeignKey("test_questions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    deleted_at = Column(DateTime, comment="Время удаления")


class TestQuestion(BaseModel):
    """Модель вопросов конкретного теста."""

    __tablename__ = "test_questions"
    __table_args__ = (UniqueConstraint("test_id", "question_id", name="unique_question_in_test"),)

    text = Column(Text)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    order_num = Column(Integer, nullable=False)
    deleted_at = Column(DateTime, comment="Время удаления")


class TestCompleted(BaseModel):
    """Модель пройденых пользователями тестов."""

    __tablename__ = "completed_tests"
    __table_args__ = (UniqueConstraint("user_id", "test_id", name="unique_test_completed"),)

    value = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    deleted_at = Column(DateTime, comment="Время удаления")
