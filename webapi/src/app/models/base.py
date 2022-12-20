from datetime import datetime

from app import db
from sqlalchemy import Column, DateTime, Integer


def fresh_timestamp() -> datetime:
    """Временная метка."""
    return datetime.utcnow


class BaseModel(db.Model):
    """Абстрактная модель с общими полями."""

    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column("Время создания", DateTime, default=fresh_timestamp)
    updated_at = Column("Время обновления", DateTime, onupdate=fresh_timestamp)
