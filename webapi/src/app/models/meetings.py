from app.models import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, Integer, SmallInteger, String, Text


class Meeting(BaseModel):
    """Запись на встречу с психологом."""

    __tablename__ = "meetings_meetings"

    client_id = Column("Клиент", Integer, ForeignKey("users_users.id"), nullable=False)
    user_id = Column("Психолог", Integer, ForeignKey("users_users.id"), nullable=False)
    type_id = Column(
        "Тип встречи",
        Integer,
        ForeignKey("meetings_meeting_types.id"),
        nullable=False,
    )
    comment = Column("Обращение к психологу", Text)
    target_test_score = Column("Бал за тест", SmallInteger, nullable=False)
    time_slot = Column("Временной слот", DateTime, nullable=False)
    deleted_at = Column("Время удаления", DateTime)


class MeetingType(BaseModel):
    """Тип встречи."""

    __tablename__ = "meetings_meeting_types"

    name = Column("Название встречи", String(256), unique=True, nullable=False)


class MeetingFeedbacksCompleted(BaseModel):
    """Обратная связь после встречи с психологом."""

    __tablename__ = "meetings_meeting_feedbacks_completed"

    meeting_id = Column("Встреча", Integer, ForeignKey("meetings_meetings.id"), nullable=False)
    user_id = Column("Клиент", Integer, ForeignKey("users_users.id"), nullable=False)
