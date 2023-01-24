from http import HTTPStatus

from app.internal.api_services import BaseAPIService
from app.internal.model_services import MeetingTypeModelService, SchemaModel
from app.models import MeetingType
from flask import abort


class MeetingTypeService(BaseAPIService):
    def __init__(self, model):
        super().__init__(model)
        self.service = MeetingTypeModelService

    def create(self, data: SchemaModel):
        meeting_type = MeetingType(**dict(data))

        meeting_type_exists = self.service.check_exists_object(self, data.name)
        if meeting_type_exists:
            return abort(HTTPStatus.CONFLICT, "Такой тип встречи уже существует!")

        self.service.create(self, meeting_type)
        return meeting_type

    def update(self, meeting_type_id: int, data: SchemaModel):
        meeting_type = self.service.get_object_or_none(self, meeting_type_id)
        if not meeting_type:
            return abort(HTTPStatus.NOT_FOUND, "Тип встречи с заданным id не существует.")

        meeting_type_exists = self.service.check_exists_object(self, data.name)
        if meeting_type_exists:
            return abort(HTTPStatus.CONFLICT, "Такой тип встречи уже существует!")

        meeting_type.from_dict(dict(data))
        self.service.update(self)
        return meeting_type


meeting_type_service = MeetingTypeService(MeetingType)
