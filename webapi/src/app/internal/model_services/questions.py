from typing import TypeVar

from app.internal.model_services import BaseModelService
from app.models import Question
from flask import abort

DataBaseModel = TypeVar("DataBaseModel")


class QuestionModelService(BaseModelService):
    """Класс для работы с моделью Question."""

    def __init__(self, model):
        super().__init__(Question)
