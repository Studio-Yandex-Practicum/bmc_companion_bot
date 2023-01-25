from http import HTTPStatus

from app.internal.api_services import BaseAPIService
from app.internal.model_services import (
    SchemaModel,
    UserModelService,
    UserRoleModelService,
    UserTimeSlotModelService,
)
from app.models import User, UserRole, UserTimeSlot
from flask import abort


class UserService(BaseAPIService):
    def __init__(self, model):
        super().__init__(model)
        self.service = UserModelService
        self.role_service = UserRoleModelService(UserRole)

    def user_create(self, data: SchemaModel):
        user = User(**dict(data))
        user_exists = self.service.check_user_exists(self, data.phone)
        if user_exists and data.phone is not None:
            return abort(HTTPStatus.CONFLICT, "Пользователь с таким номером телефона уже есть!")
        role = self.role_service.get_object_or_none(data.role_id)
        if role is None:
            return abort(HTTPStatus.NOT_FOUND, "Такой роли нет!")
        self.service.create(self, user)
        return user

    def user_update(self, id: int, data: SchemaModel):
        user = self.service.get_object_or_none(self, id)
        if user is None:
            return abort(HTTPStatus.NOT_FOUND, "Пользователя с заданным id не существует.")
        phone_in_use = self.service.check_user_exists(self, data.phone)
        if phone_in_use and data.phone is not None:
            return abort(HTTPStatus.CONFLICT, "Пользователь с таким номером телефона уже есть!")
        role = self.role_service.get_object_or_none(data.role_id)
        if role is None:
            return abort(HTTPStatus.NOT_FOUND, "Такой роли нет!")
        user.from_dict(dict(data))
        self.service.update(self)
        return user


class UserTimeSlotService(BaseAPIService):
    def __init__(self, model):
        super().__init__(model)
        self.service = UserTimeSlotModelService

    def user_time_slot_create(self, data: SchemaModel):
        time_slot = UserTimeSlot(**dict(data))
        self.service.check_timeslot_exists(self, data.date_start, data.date_end, data.user_id)
        self.service.create(self, time_slot)
        return time_slot

    def user_time_slot_update(self, id: int, data: SchemaModel):
        time_slot = self.service.get_object_or_none(self, id)
        if time_slot is None:
            return abort(HTTPStatus.NOT_FOUND, "Временногослота с заданным id не существует.")
        self.service.check_timeslot_exists(self, data.date_start, data.date_end, data.user_id)
        time_slot.from_dict(dict(data))
        self.service.update(self)
        return time_slot


user_service = UserService(User)
user_time_slot_service = UserTimeSlotService(UserTimeSlot)
