from typing import Optional

from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    """Базовая схема."""

    pass


class StatusResponse(BaseModel):
    """
    Формат ответа для запросов, в которых не требуется отдавать данные
    """

    status: str = "ok"
    message: Optional[str] = None
    warning_info: list[dict] = Field(default_factory=list)
