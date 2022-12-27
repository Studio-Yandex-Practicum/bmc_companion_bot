from typing import List, Optional, TypeVar

from app.utils import get_paginated_list
from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    """Базовая схема."""

    pass


ListElement = TypeVar("ListElement", bound=BaseModel)


class GetMultiQueryParams(BaseModel):
    """Схема параметров запроса."""

    start: int = Field(1, description="Смещение выбоки объектов")
    limit: int = Field(10, le=100, description="Количество объектов на одной странице")
    count: int = Field(None, description="Общее количество объектов")
    previous: str = Field(None, description="Предыдущая страница")
    next: str = Field(None, description="Следующая страница")


class ObjectList(GetMultiQueryParams):
    """Схема для получения списка элементов."""

    data: List[ListElement]

    def pagination(self, data, url, query):
        return get_paginated_list(data, url, query)

    class Config:
        orm_mode = True


class StatusResponse(BaseModel):
    """
    Формат ответа для запросов, в которых не требуется отдавать данные
    """

    status: str = "ok"
    message: Optional[str] = None
    warning_info: list[dict] = Field(default_factory=list)
