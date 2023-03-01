from app import db
from app.models import BaseModel


class Meeting(BaseModel):
    """Запись на встречу с психологом."""

    __tablename__ = "meetings"

    client_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    type_id = db.Column(
        db.Integer,
        db.ForeignKey("meeting_types.id"),
        nullable=False,
    )
    comment = db.Column(db.Text)
    target_test_score = db.Column(db.SmallInteger, nullable=False)
    time_slot = db.Column(db.DateTime, nullable=False)
    deleted_at = db.Column(db.DateTime)


class MeetingType(BaseModel):
    """Тип встречи."""

    __tablename__ = "meeting_types"

    name = db.Column(db.String(256), unique=True, nullable=False)


class MeetingFeedbacksCompleted(BaseModel):
    """Обратная связь после встречи с психологом."""

    __tablename__ = "meeting_feedbacks_completed"

    meeting_id = db.Column(db.Integer, db.ForeignKey("meetings.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


class PsychologistInfo(BaseModel):
    """Данные о календаре психолога."""

    __tablename__ = "psychologist_info"

    cal_link = db.Column(db.Text)
    cal_username = db.Column(db.Text)
    cal_pass = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    deleted_at = db.Column(db.DateTime)


class MeetingReview(BaseModel):
    """Оценка встречи с психологом."""

    __tablename__ = "assessment_of_the_meeting"

    meeting_id = db.Column(db.Integer, db.ForeignKey("meetings.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    text = db.Column(db.Text)
    score = db.Column(db.Integer)
