from http import HTTPStatus

from app.internal.api_services import BaseAPIService
from app.internal.model_services import (
    CompletedModelService,
    ProgressModelService,
    QuestionModelService,
    SchemaModel,
    TestModelService,
    UserModelService,
)
from app.models import Question, Test, TestCompleted, TestProgress, User
from flask import abort


class TestProgressService(BaseAPIService):
    def __init__(self, model):
        super().__init__(model)
        self.service = ProgressModelService
        self.question_service = QuestionModelService(Question)
        self.user_service = UserModelService(User)

    def progress_create(self, data: SchemaModel):
        progress = TestProgress(**dict(data))
        user = self.user_service.get_object_or_none(data.user_id)
        if user is None:
            return abort(HTTPStatus.NOT_FOUND, "Пользователя с заданным id не существует.")
        question = self.question_service.get_object_or_none(data.test_question_id)
        if question is None:
            return abort(HTTPStatus.NOT_FOUND, "Вопроса с заданным id не существует.")
        progress_exists = self.service.check_progress_exists(self, data)
        if progress_exists:
            return abort(HTTPStatus.CONFLICT, "Прогресс уже существует.")
        self.service.create(self, progress)
        return progress

    def progress_update(self, id: int, data: SchemaModel):
        progress = self.service.get_object_or_none(self, id)
        if progress is None:
            return abort(HTTPStatus.NOT_FOUND, "Прогресса с заданным id не существует.")
        question = self.question_service.get_object_or_none(data.test_question_id)
        if question is None:
            return abort(HTTPStatus.NOT_FOUND, "Вопроса с заданным id не существует.")
        progress_exists = self.service.check_progress_exists_for_update(self, progress, data)
        if progress_exists:
            return abort(HTTPStatus.CONFLICT, "Прогресс уже существует.")
        progress.from_dict(dict(data))
        self.service.update(self)
        return progress


class TestCompletedService(BaseAPIService):
    def __init__(self, model):
        super().__init__(model)
        self.service = CompletedModelService
        self.user_service = UserModelService(User)
        self.test_service = TestModelService(Test)

    def completed_create(self, data: SchemaModel):
        test_completed = TestCompleted(**dict(data))
        user = self.user_service.get_object_or_none(data.user_id)
        if user is None:
            return abort(HTTPStatus.NOT_FOUND, "Пользователя с заданным id не существует.")
        test = self.test_service.get_object_or_none(data.test_id)
        if test is None:
            return abort(HTTPStatus.NOT_FOUND, "Теста с заданным id не существует.")
        test_completed_exists = self.service.check_test_completed_exists(self, data)
        if test_completed_exists:
            return abort(HTTPStatus.CONFLICT, "Тест уже пройден.")
        self.service.create(self, test_completed)
        return test_completed

    def completed_update(self, id: int, data: SchemaModel):
        test_completed = self.service.get_object_or_none(self, id)
        if test_completed is None:
            return abort(HTTPStatus.NOT_FOUND, "Завершенного теста с заданным id не существует.")
        test_completed.from_dict(dict(data))
        self.service.update(self)
        return test_completed


test_progress_service = TestProgressService(TestProgress)
test_completed_service = TestCompletedService(TestCompleted)
