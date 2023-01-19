from datetime import datetime
from http import HTTPStatus

from app.internal.model_services import (
    BaseModelService,
    CompletedModelService,
    ProgressModelService,
    QuestionModelService,
    SchemaModel,
    TestModelService,
    UserModelService,
    UserRoleModelService,
    UserTimeSlotModelService,
)
from app.models import TestCompleted, TestProgress, User, UserTimeSlot
from flask import abort


class BaseAPIService:
    def __init__(self, model):
        self.model = model
        self.service = BaseModelService(self.model)

    def get_object_by_id(self, id: int):
        db_object = self.service.get_object_or_none(self, id)
        if db_object is None:
            return abort(HTTPStatus.NOT_FOUND, "Объекта с заданным id не существует.")
        return db_object

    def get_paginated_objects_list(self, schema_singl_object, schema_list, url, query):
        db_objects = self.service.get_all_objects(self)
        db_objects_data = [(dict(schema_singl_object.from_orm(object))) for object in db_objects]
        paginated_data = schema_list.pagination(self, data=db_objects_data, url=url, query=query)
        return paginated_data

    def remove_object(self, id: int):
        db_object = self.service.get_object_or_none(self, id)
        if db_object is None:
            return abort(HTTPStatus.NOT_FOUND, "Объекта с заданным id не существует.")
        if db_object.deleted_at is not None:
            return abort(HTTPStatus.CONFLICT, "Объект уже заблокирован!")
        db_object.deleted_at = datetime.utcnow()
        self.service.update(self)


class TestProgressService(BaseAPIService):
    def __init__(self, model):
        super().__init__(model)
        self.service = ProgressModelService
        self.question_service = QuestionModelService
        self.user_service = UserModelService

    def progress_create(self, data: SchemaModel):
        progress = TestProgress(**dict(data))
        user = self.user_service.get_object_or_none(self, data.user_id)
        if user is None:
            return abort(HTTPStatus.NOT_FOUND, "Пользователя с заданным id не существует.")
        question = self.question_service.get_object_or_none(self, data.test_question_id)
        if question is None:
            return abort(HTTPStatus.NOT_FOUND, "Вопроса с заданным id не существует.")
        progress_exists = self.service.check_progress_exists(self, data)
        if progress_exists:
            return abort(HTTPStatus.CONFLICT, "Прогресс уже существует.")
        self.service.create(self, progress)
        return progress

    def progress_update(self, id: int, data: SchemaModel):
        progress = self.service.get_object_or_none(self, id)
        if progress is None:
            return abort(HTTPStatus.NOT_FOUND, "Прогресса с заданным id не существует.")
        question = self.question_service.get_object_or_none(self, data.test_question_id)
        if question is None:
            return abort(HTTPStatus.NOT_FOUND, "Вопроса с заданным id не существует.")
        progress_exists = self.service.check_progress_exists_for_update(self, progress, data)
        if progress_exists:
            return abort(HTTPStatus.CONFLICT, "Прогресс уже существует.")
        progress.from_dict(dict(data))
        self.service.update(self)
        return progress


class TestCompletedService(BaseAPIService):
    def __init__(self, model):
        super().__init__(model)
        self.service = CompletedModelService
        self.user_service = UserModelService
        self.test_service = TestModelService

    def completed_create(self, data: SchemaModel):
        test_completed = TestCompleted(**dict(data))
        user = self.user_service.get_object_or_none(self, data.user_id)
        if user is None:
            return abort(HTTPStatus.NOT_FOUND, "Пользователя с заданным id не существует.")
        test = self.test_service.get_object_or_none(self, data.test_id)
        if test is None:
            return abort(HTTPStatus.NOT_FOUND, "Теста с заданным id не существует.")
        test_completed_exists = self.service.check_test_completed_exists(self, data)
        if test_completed_exists:
            return abort(HTTPStatus.CONFLICT, "Тест уже пройден.")
        self.service.create(self, test_completed)
        return test_completed

    def completed_update(self, id: int, data: SchemaModel):
        test_completed = self.service.get_object_or_none(self, id)
        if test_completed is None:
            return abort(HTTPStatus.NOT_FOUND, "Завершенного теста с заданным id не существует.")
        test_completed.from_dict(dict(data))
        self.service.update(self)
        return test_completed


class UserService(BaseAPIService):
    def __init__(self, model):
        super().__init__(model)
        self.service = UserModelService
        self.role_service = UserRoleModelService

    def user_create(self, data: SchemaModel):
        user = User(**dict(data))
        user_exists = self.service.check_user_exists(self, data.phone)
        if user_exists and data.phone is not None:
            return abort(HTTPStatus.CONFLICT, "Пользователь с таким номером телефона уже есть!")
        role = self.role_service.get_object_or_none(self, data.role_id)
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
        role = self.role_service.get_object_or_none(self, data.role_id)
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
test_progress_service = TestProgressService(TestProgress)
test_completed_service = TestCompletedService(TestCompleted)
user_time_slot_service = UserTimeSlotService(UserTimeSlot)
