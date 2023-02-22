from http import HTTPStatus

from app.internal.api_services import user_time_slot_service
from app.models import UserTimeSlot
from app.schemas.core import GetMultiQueryParams, StatusResponse
from app.schemas.user_time_slot import (
    UserTimeSlotCreate,
    UserTimeSlotList,
    UserTimeSlotResponse,
    UserTimeSlotUpdate,
)
from flask import abort
from flask_pydantic import validate
from flask_restful import Resource

FORMAT = "%Y/%m/%d %H:%M:%S"


def get_object_by_id(obj_id):
    """Получить объект по id."""
    obj = UserTimeSlot.query.get(obj_id)
    if not obj:
        return abort(HTTPStatus.NOT_FOUND, "Слота с заданным id не существует.")
    return obj


def check_object(body):
    """Проверка на существование объекта."""
    if body.date_start:
        return abort(HTTPStatus.CONFLICT, "Такой временной слот уже существует!")


def check_delete_object(obj):
    if obj.deleted_at is not None:
        return abort(HTTPStatus.NOT_FOUND, "Слот с заданным id заблокирован.")


class UserTimeSlotAPI(Resource):
    @validate()
    def get(self, id: int) -> UserTimeSlotResponse:
        """Получение данных слота по id."""
        slot = user_time_slot_service.get_object_by_id(id)
        return UserTimeSlotResponse.from_orm(slot)

    @validate()
    def patch(self, id: int, body: UserTimeSlotUpdate) -> UserTimeSlotResponse:
        """Изменение данных определенного слота по id."""
        slot = user_time_slot_service.user_time_slot_update(id, body)
        return UserTimeSlotResponse.from_orm(slot)

    @validate()
    def delete(self, id: int) -> StatusResponse:
        """Soft-delete временного слота."""
        user_time_slot_service.remove_object(id)
        return StatusResponse(message="Временной слот заблокирован.")


class UserTimeSlotAPIList(Resource):
    @validate(on_success_status=HTTPStatus.CREATED)
    def post(self, body: UserTimeSlotCreate) -> UserTimeSlotResponse:
        """Создание слота."""
        slot = user_time_slot_service.user_time_slot_create(body)
        return UserTimeSlotResponse.from_orm(slot)

    @validate()
    def get(self, query: GetMultiQueryParams) -> UserTimeSlotList:
        """Получение всех слотов."""
        paginated_data = user_time_slot_service.get_paginated_objects_list(
            schema_singl_object=UserTimeSlotResponse,
            schema_list=UserTimeSlotList,
            url="/api/v1/slots/",
            query=query,
        )
        return UserTimeSlotList(**paginated_data)
