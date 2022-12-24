from http import HTTPStatus
from typing import Optional

from pydantic import BaseModel, Field


class StatusResponse(BaseModel):
    """
    Формат ответа для запросов, в которых не требуется отдавать данные
    """

    status: int = HTTPStatus.OK
    warning: Optional[str] = None
    warning_info: list[dict] = Field(default_factory=list)
