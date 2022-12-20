import uuid

from app import db
from sqlalchemy.dialects.postgresql import UUID


class General(db.Model):
    """Абстрактная модель.
    Attributes:
        id(uuid):
            Уникальный идентификационный номер.
    """

    __abstract__ = True
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
