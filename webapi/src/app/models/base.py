from datetime import datetime

from app import db


def fresh_timestamp() -> datetime:
    """Временная метка."""
    return datetime.utcnow


class BaseModel(db.Model):
    """Абстрактная модель с общими полями."""

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=fresh_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=fresh_timestamp())

    def from_dict(self, data):
        for key, item in data.items():
            setattr(self, key, item)
