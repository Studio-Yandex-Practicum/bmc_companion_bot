from http import HTTPStatus

from app.internal.api_services import BaseAPIService
from app.internal.model_services import (
    MeetingFeedbackModelService,
    MeetingModelService,
    MeetingTypeModelService,
    SchemaModel,
)
from app.models import Meeting, MeetingFeedback, MeetingType
from flask import abort


class MeetingService(BaseAPIService):
    def __init__(self, model):
        super().__init__(model)
        self.service = MeetingModelService

    def create(self, data: SchemaModel):
        meeting = Meeting(**dict(data))
        self.service.create(self, meeting)
        return meeting

    def update(self, meeting_id: int, data: SchemaModel):
        meeting = self.service.get_object_or_none(self, meeting_id)
        meeting.from_dict(dict(data))
        self.service.update(self)
        return meeting


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


class MeetingFeedbackService(BaseAPIService):
    def __init__(self, model):
        super().__init__(model)
        self.service = MeetingFeedbackModelService

    def create(self, data: SchemaModel):
        meeting_feedback = MeetingFeedback(**dict(data))
        self.service.create(self, meeting_feedback)
        return meeting_feedback

    def update(self, meeting_feedback_id: int, data: SchemaModel):
        meeting_feedback = self.service.get_object_or_none(self, meeting_feedback_id)
        meeting_feedback.from_dict(dict(data))
        self.service.update(self)
        return meeting_feedback


meeting_service = MeetingService(Meeting)
meeting_type_service = MeetingTypeService(MeetingType)
meeting_feedback_service = MeetingFeedbackService(MeetingFeedback)
