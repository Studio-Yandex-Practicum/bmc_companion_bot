from http import HTTPStatus

from app.db.pg import db
from app.models import MeetingType
from app.schemas.core import GetMultiQueryParams, StatusResponse
from app.schemas.meetings import (
    MeetingTypeCreate,
    MeetingTypeList,
    MeetingTypeResponse,
    MeetingTypeUpdate,
)
from flask import abort
from flask_pydantic import validate
from flask_restful import Resource


class MeetingTypeAPI(Resource):
    @validate()
    def get(self, meeting_type_id: int) -> MeetingTypeResponse:
        """Получение данных о типе встречи по id."""
        meeting_type = MeetingType.query.get(meeting_type_id)
        if not meeting_type:
            return abort(HTTPStatus.NOT_FOUND, "Тип встречи с заданным id не существует.")

        return MeetingTypeResponse.from_orm(meeting_type)

    @validate()
    def patch(self, meeting_type_id: int, body: MeetingTypeUpdate) -> MeetingTypeResponse:
        """Изменение данных о типе встречи по id."""
        meeting_type = MeetingType.query.get(meeting_type_id)
        if not meeting_type:
            return abort(HTTPStatus.NOT_FOUND, "Тип встречи с заданным id не существует.")

        meeting_type_exists = (
            db.session.query(MeetingType).where(MeetingType.name == body.name).first()
        )
        if not meeting_type_exists:
            return abort(HTTPStatus.CONFLICT, "Такой тип встречи уже есть!")

        meeting_type.from_dict(dict(body))
        db.session.commit()
        return MeetingTypeResponse.from_orm(meeting_type)

    @validate()
    def delete(self, meeting_type_id: int) -> StatusResponse:
        """Hard-delete типа встречи."""
        meeting_type = MeetingType.query.get(meeting_type_id)
        if not meeting_type:
            return abort(HTTPStatus.NOT_FOUND, "Вопроса с заданным id не существует.")

        db.session.delete(meeting_type)
        db.session.commit()
        return StatusResponse(
            warning="Ресурс удалён.",
        )


class MeetingTypeAPIList(Resource):
    @validate()
    def get(self, query: GetMultiQueryParams) -> MeetingTypeList:
        """Получение список всех типов встречи."""
        meeting_types = MeetingType.query.all()
        meeting_type_data = [
            (dict(MeetingTypeResponse.from_orm(meeting_type))) for meeting_type in meeting_types
        ]
        paginated_data = MeetingTypeList.pagination(
            self, data=meeting_type_data, url="/api/v1/meeting_types/", query=query
        )
        return MeetingTypeList(**paginated_data)

    @validate(on_success_status=HTTPStatus.CREATED)
    def post(self, body: MeetingTypeCreate) -> MeetingTypeResponse:
        """Создаёт новый тип встречи."""
        meeting_type = MeetingType()

        meeting_type_exists = (
            db.session.query(MeetingType).where(MeetingType.name == body.name).first()
        )
        if not meeting_type_exists:
            return abort(HTTPStatus.CONFLICT, "Такой тип встречи уже есть!")

        meeting_type.from_dict(dict(body))
        db.session.add(meeting_type)
        db.session.commit()
        return MeetingTypeResponse.from_orm(meeting_type)
