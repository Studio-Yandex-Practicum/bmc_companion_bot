from datetime import datetime
from http import HTTPStatus

from app.db.pg import db
from app.internal.model_services import BaseModelService
from app.models import User, UserRole, UserTimeSlot
from flask import abort


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
