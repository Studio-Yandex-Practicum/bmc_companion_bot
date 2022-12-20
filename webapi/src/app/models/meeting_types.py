import uuid

from app import db
from sqlalchemy.dialects.postgresql import UUID


class MeetingType(db.Model):
    """Название типа встречи.
    Attributes:
        id(uuid):
            Уникальный идентификационный номер. Обязательное поле.
    """

    __tablename__ = "meeting_types"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
