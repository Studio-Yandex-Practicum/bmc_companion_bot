from datetime import datetime
from http import HTTPStatus

from app.db.pg import db
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
        slot = get_object_by_id(id)
        return UserTimeSlotResponse.from_orm(slot)

    @validate()
    def patch(self, id: int, body: UserTimeSlotUpdate) -> UserTimeSlotResponse:
        """Изменение данных определенного слота по id."""
        slot = get_object_by_id(id)
        check_delete_object(slot)
        # check_exists_object(body)
        slot.from_dict(dict(body))
        slot.updated_at = datetime.utcnow().strftime(FORMAT)
        db.session.commit()
        return UserTimeSlotResponse.from_orm(slot)

    @validate()
    def delete(self, id: int) -> StatusResponse:
        """Soft-delete вопроса."""
        slot = get_object_by_id(id)
        check_delete_object(slot)
        slot.deleted_at = datetime.utcnow().strftime(FORMAT)
        db.session.commit()
        message = StatusResponse(
            warning="Ресурс заблокирован.",
        )
        return message


class UserTimeSlotAPIList(Resource):
    @validate(on_success_status=HTTPStatus.CREATED)
    def post(self, body: UserTimeSlotCreate) -> UserTimeSlotResponse:
        """Создание слота."""
        slot = UserTimeSlot()
        slot_exists = (
            db.session.query(UserTimeSlot)
            .where(
                UserTimeSlot.date_start == body.date_start
                and UserTimeSlot.date_end == body.date_end
            )
            .first()
        )
        if slot_exists is not None:
            return abort(HTTPStatus.CONFLICT, "Такой слот уже есть!")
        slot.from_dict(dict(body))
        db.session.add(slot)
        slot.created_at = datetime.utcnow().strftime(FORMAT)
        db.session.commit()
        return UserTimeSlotResponse.from_orm(slot)

    @validate()
    def get(self, query: GetMultiQueryParams) -> UserTimeSlotList:
        """Получение всех слотов."""
        slot_db = UserTimeSlot.query.filter_by(deleted_at=None).all()
        slot_data = [(dict(UserTimeSlotResponse.from_orm(slot))) for slot in slot_db]
        paginated_data = UserTimeSlotList.pagination(
            self, data=slot_data, url="/api/v1/slots/", query=query
        )
        return UserTimeSlotList(**paginated_data)
