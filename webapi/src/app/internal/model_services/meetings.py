from app.db.pg import db
from app.internal.model_services import BaseModelService
from app.models import Meeting, MeetingFeedback, MeetingType
from app.schemas.meetings import MeetingTypeList


class MeetingModelService(BaseModelService):
    def __init__(self, model):
        super().__init__(Meeting)


class MeetingTypeModelService(BaseModelService):
    def __init__(self, model):
        super().__init__(MeetingType)

    def check_exists_object(self, name: str) -> None | MeetingTypeList:
        """Проверяет наличее объекта по name."""
        return db.session.query(self.model).where(self.model.name == name).first()


class MeetingFeedbackService(BaseModelService):
    def __init__(self, model):
        super().__init__(MeetingFeedback)
