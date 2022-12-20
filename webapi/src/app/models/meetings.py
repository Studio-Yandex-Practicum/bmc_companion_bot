import uuid
from datetime import datetime

from app import db
from sqlalchemy.dialects.postgresql import UUID


class Meeting(db.Model):
    """Запись на консультацию к психологу.
    Attributes:
        id(uuid):
            Уникальный идентификационный номер. Обязательное поле.
        client_id(uuid):
            Клиент - берётся из модели `User`. Обязательное поле.
        user_id(uuid):
            Психолог - берётся из модели `User`. Обязательное поле.
        type_id(uuid):
            Тип встречи - берётся из модели `MeetingTapy`. Обязательное поле.
        comment(str):
            Комментарий клиента по результату встречи. Не обязательное поле.
        target_test_score(int):
            Бал за тест. Обязательное поле.
        time_slot(DateTime):
            Временной слот на который записан клиент. Обязательное поле.
        created_at(DateTime):
           Время создания записи. Обязательное поле.
        deleted_at(DateTime):
            Время удаления записи. Не обязательное поле.
    """

    __tablename__ = "meetings"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    client_id = db.Column("Клиент", UUID, db.ForeignKey("users.id"), nullable=False)
    user_id = db.Column("Психолог", UUID, db.ForeignKey("users.id"), nullable=False)
    type_id = db.Column("Тип встречи", UUID, db.ForeignKey("meeting_types.id"), nullable=False)
    comment = db.Column("Комментарий", db.Text, nullable=True)
    target_test_score = db.Column("Бал за тест", db.SmallInteger, nullable=False)
    time_slot = db.Column("Временной слот", db.DateTime, nullable=False)
    created_at = db.Column("Время создания", db.DateTime, default=datetime.now)
    deleted_at = db.Column("Время удаления", db.DateTime, nullable=True)
