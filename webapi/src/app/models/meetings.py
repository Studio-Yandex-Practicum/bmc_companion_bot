from app.models import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, Integer, SmallInteger, String, Text


class Meeting(BaseModel):
    """Запись на встречу с психологом."""

    __tablename__ = "meetings"
    __table_args__ = {"schema": "meetings"}

    client_id = Column("Клиент", Integer, ForeignKey("general.users.id"), nullable=False)
    user_id = Column("Психолог", Integer, ForeignKey("general.users.id"), nullable=False)
    type_id = Column(
        "Тип встречи",
        Integer,
        ForeignKey("meetings.meeting_types.id"),
        nullable=False,
    )
    comment = Column("Обращение к психологу", Text)
    target_test_score = Column("Бал за тест", SmallInteger, nullable=False)
    time_slot = Column("Временной слот", DateTime, nullable=False)
    deleted_at = Column("Время удаления", DateTime)


class MeetingType(BaseModel):
    """Тип встречи."""

    __tablename__ = "meeting_types"
    __table_args__ = {"schema": "meetings"}

    name = Column("Название встречи", String(256))


class MeetingFeedbacksCompleted(BaseModel):
    """Обратная связь после встречи с психологом."""

    __tablename__ = "meeting_feedbacks_completed"
    __table_args__ = {"schema": "meetings"}

    meeting_id = Column("Встреча", Integer, ForeignKey("meetings.meetings.id"), nullable=False)
    user_id = Column("Клиент", Integer, ForeignKey("general.users.id"), nullable=False)
