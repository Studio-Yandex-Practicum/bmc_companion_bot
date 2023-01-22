from typing import TypeVar

from app.db.pg import db
from app.internal.model_services import BaseModelService
from app.models import Test, TestCompleted, TestProgress

DataBaseModel = TypeVar("DataBaseModel")
SchemaModel = TypeVar("SchemaModel")


class TestModelService(BaseModelService):
    """Класс для работы с моделью Test."""

    def __init__(self, model):
        super().__init__(Test)


class ProgressModelService(BaseModelService):
    """Класс для работы с моделью TestProgress"""

    def __init__(self, model):
        super().__init__(TestProgress)

    def check_progress_exists(self, data: SchemaModel):
        progress = (
            db.session.query(self.model)
            .where(
                self.model.user_id == data.user_id,
                self.model.test_question_id == data.test_question_id,
            )
            .first()
        )
        return progress

    def check_progress_exists_for_update(self, progress: DataBaseModel, data: SchemaModel):
        progress = (
            db.session.query(self.model)
            .where(
                self.model.user_id == progress.user_id,
                self.model.test_question_id == data.test_question_id,
            )
            .first()
        )
        return progress


class CompletedModelService(BaseModelService):
    """Класс для работы с моделью TestCompleted."""

    def __init__(self, model):
        super().__init__(TestCompleted)

    def check_test_completed_exists(self, data: SchemaModel):
        test_completed = (
            db.session.query(self.model)
            .where(
                self.model.user_id == data.user_id,
                self.model.test_id == data.test_id,
            )
            .first()
        )
        return test_completed
