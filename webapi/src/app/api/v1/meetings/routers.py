from http import HTTPStatus

from app.internal.api_services import meeting_service, meeting_type_service
from app.schemas.core import GetMultiQueryParams
from app.schemas.meetings import (
    MeetingCreate,
    MeetingList,
    MeetingResponse,
    MeetingTypeCreate,
    MeetingTypeList,
    MeetingTypeResponse,
    MeetingTypeUpdate,
    MeetingUpdate,
)
from flask_pydantic import validate
from flask_restful import Resource


class MeetingApiList(Resource):
    @validate()
    def get(self, query: GetMultiQueryParams) -> MeetingList:
        """Получить список встреч."""
        paginated_data = meeting_service.get_paginated_objects_list(
            schema_singl_object=MeetingResponse,
            schema_list=MeetingList,
            url="/api/v1/meetings/",
            query=query,
        )
        return MeetingList(**paginated_data)

    @validate(on_success_status=HTTPStatus.CREATED)
    def post(self, body: MeetingCreate) -> MeetingResponse:
        """Создать новый тип встречи."""
        meeting = meeting_service.create(body)
        return MeetingResponse.from_orm(meeting)


class MeetingApiDetail(Resource):
    @validate()
    def get(self, meeting_id: int) -> MeetingResponse:
        """Получить встречу по id."""
        meeting = meeting_service.get_object_by_id(meeting_id)
        return MeetingResponse.from_orm(meeting)

    @validate()
    def patch(self, meeting_id: int, body: MeetingUpdate) -> MeetingResponse:
        """Изменить данные о встречи по id."""
        meeting = meeting_service.update(meeting_id, body)
        return MeetingResponse.from_orm(meeting)


class MeetingTypeApiList(Resource):
    @validate()
    def get(self, query: GetMultiQueryParams) -> MeetingTypeList:
        """Получить список всех типов встречи."""
        paginated_data = meeting_type_service.get_paginated_objects_list(
            schema_singl_object=MeetingTypeResponse,
            schema_list=MeetingTypeList,
            url="/api/v1/meeting_types/",
            query=query,
        )
        return MeetingTypeList(**paginated_data)

    @validate(on_success_status=HTTPStatus.CREATED)
    def post(self, body: MeetingTypeCreate) -> MeetingTypeResponse:
        """Создать новый тип встречи."""
        meeting_type = meeting_type_service.create(body)
        return MeetingTypeResponse.from_orm(meeting_type)


class MeetingTypeApiDetail(Resource):
    @validate()
    def get(self, meeting_type_id: int) -> MeetingTypeResponse:
        """Получить тип встречи по id."""
        meeting_type = meeting_type_service.get_object_by_id(meeting_type_id)
        return MeetingTypeResponse.from_orm(meeting_type)

    @validate()
    def patch(self, meeting_type_id: int, body: MeetingTypeUpdate) -> MeetingTypeResponse:
        """Изменить данные о типе встречи по id."""
        meeting_type = meeting_type_service.update(meeting_type_id, body)
        return MeetingTypeResponse.from_orm(meeting_type)
