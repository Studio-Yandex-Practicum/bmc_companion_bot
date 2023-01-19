from datetime import datetime
from http import HTTPStatus
from typing import TypeVar

from app.db.pg import db
from app.models import (
    Question,
    Test,
    TestCompleted,
    TestProgress,
    User,
    UserRole,
    UserTimeSlot,
)
from flask import abort

DataBaseModel = TypeVar("DataBaseModel")
SchemaModel = TypeVar("SchemaModel")


class BaseModelService:
    """Базовый класс для работы с моделями."""

    def __init__(self, model):
        self.model = model

    def get_object_or_none(self, id: int):
        db_object = self.model.query.filter_by(id=id).first()
        return db_object

    def get_all_objects(self):
        db_objects = self.model.query.all()
        return db_objects

    def create(self, data: DataBaseModel):
        db.session.add(data)
        db.session.commit()
        return data

    def update(self):
        db.session.commit()


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


class UserModelService(BaseModelService):
    """Класс для работы с моделью User."""

    def __init__(self, model):
        super().__init__(User)

    def check_user_exists(self, phone: int):
        user = db.session.query(self.model).where(self.model.phone == phone).first()
        return user


class UserRoleModelService(BaseModelService):
    """Класс для работы с моделью UserRole."""

    def __init__(self, model):
        super().__init__(UserRole)


class QuestionModelService(BaseModelService):
    """Класс для работы с моделью Question."""

    def __init__(self, model):
        super().__init__(Question)


class TestModelService(BaseModelService):
    """Класс для работы с моделью Test."""

    def __init__(self, model):
        super().__init__(Test)


class UserTimeSlotModelService(BaseModelService):
    """Класс для работы с моделью Test."""

    def __init__(self, model):
        super().__init__(UserTimeSlot)

    def check_timeslot_exists(self, date_start: datetime, date_end: datetime, user_id: int):
        time_slot = (
            db.session.query(self.model)
            .where(
                self.model.date_start == date_start,
                self.model.date_end == date_end,
                self.model.user_id == user_id,
            )
            .first()
        )
        if time_slot is not None:
            return abort(HTTPStatus.CONFLICT, "Такой временной слот уже существует.")
