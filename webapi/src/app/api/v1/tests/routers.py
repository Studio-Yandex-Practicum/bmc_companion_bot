from datetime import datetime
from http import HTTPStatus

from app.db.pg import db
from app.models import Question, Test, TestCompleted, TestProgress, User
from app.schemas.core import GetMultiQueryParams, StatusResponse
from app.schemas.tests import (
    TestCompletedBare,
    TestCompletedCreate,
    TestCompletedFull,
    TestCompletedList,
    TestCompletedUpdate,
    TestCreate,
    TestList,
    TestProgressBare,
    TestProgressCreate,
    TestProgressFull,
    TestProgressList,
    TestProgressUpdate,
    TestResponse,
)
from flask import abort
from flask_pydantic import validate
from flask_restful import Resource

DT_FORMAT = "%Y/%m/%d %H:%M:%S"


class TestAPI(Resource):
    @validate()
    def get(self, test_id) -> TestResponse:
        test = Test.query.filter_by(id=test_id).one_or_none()
        if test.deleted_at is not None:
            return abort(HTTPStatus.NOT_FOUND, "Данный тест был удален!")
        return TestResponse.from_orm(test)

    @validate()
    def delete(self, test_id) -> StatusResponse:
        test = Test.query.filter_by(id=test_id).one_or_none()
        test.deleted_at = datetime.utcnow().strftime(DT_FORMAT)
        db.session.commit()
        message = StatusResponse(
            warning="Ресурс заблокирован.",
        )
        return message

    @validate()
    def patch(self, test_id, body: TestCreate) -> TestResponse:
        test = Test.query.filter_by(id=test_id).one_or_none()
        if test.deleted_at is not None:
            return abort(HTTPStatus.NOT_FOUND, "Данный тест был удален!")
        test.from_dict(dict(body))
        test.updated_at = datetime.utcnow().strftime(DT_FORMAT)
        db.session.commit()
        return TestCreate.from_orm(test)


class TestAPIList(Resource):
    @validate()
    def get(self, query: GetMultiQueryParams) -> TestList:
        test_db = Test.query.filter_by(deleted_at=None).all()
        test_data = [(dict(TestResponse.from_orm(test))) for test in test_db]
        paginated_data = TestList.pagination(
            self, data=test_data, url="/api/v1/tests/", query=query
        )
        return TestList(**paginated_data)

    @validate()
    def post(self, body: TestCreate) -> TestResponse:
        test = Test()
        test.from_dict(dict(body))
        db.session.add(test)
        db.session.commit()
        return TestResponse.from_orm(test)


class TestProgressAPI(Resource):
    @validate()
    def get(self, progress_id: int) -> TestProgressFull:
        """Получение данных определенного прогресса по id."""
        test_progress = TestProgress.query.get(progress_id)
        if test_progress is None:
            return abort(HTTPStatus.NOT_FOUND, "Прогресса с заданным id не существует.")
        return TestProgressFull.from_orm(test_progress)

    @validate()
    def patch(self, progress_id: int, body: TestProgressUpdate) -> TestProgressFull:
        """Изменение данных определенного прогресса по id."""
        progress = TestProgress.query.get(progress_id)
        question = db.session.query(Question).where(Question.id == body.test_question_id).first()
        if question is None:
            return abort(HTTPStatus.NOT_FOUND, "Вопроса с заданным id не существует.")
        progress_exists = (
            db.session.query(TestProgress)
            .where(
                TestProgress.user_id == progress.user_id,
                TestProgress.test_question_id == body.test_question_id,
            )
            .first()
        )
        if progress_exists:
            return abort(HTTPStatus.CONFLICT, "Прогресс уже существует.")
        progress.from_dict(dict(body))
        db.session.commit()
        return TestProgressFull.from_orm(progress)

    @validate()
    def delete(self, progress_id: int):
        """Блокировка прогресса пользователя."""
        progress = TestProgress.query.get(progress_id)
        if progress is None:
            return abort(HTTPStatus.NOT_FOUND, "Прогресса с заданным id не существует.")
        if progress.deleted_at is not None:
            return abort(HTTPStatus.CONFLICT, "Прогресс уже заблокирован!")
        progress.deleted_at = datetime.utcnow()
        db.session.commit()
        return StatusResponse(warning="Прогресс заблокирован.")


class TestProgressAPIList(Resource):
    @validate()
    def get(self, query: GetMultiQueryParams) -> TestProgressList:
        """Получение списка прогресса всех пользователей."""
        test_progress_db = TestProgress.query.all()
        test_data = [(dict(TestProgressBare.from_orm(test))) for test in test_progress_db]
        paginated_data = TestList.pagination(
            self, data=test_data, url="/api/v1/tests/progress/", query=query
        )
        return TestProgressList(**paginated_data)

    @validate(on_success_status=HTTPStatus.CREATED)
    def post(self, body: TestProgressCreate) -> TestProgressBare:
        """Создание прогресса прохождения теста пользователем."""
        progress = TestProgress()
        user = db.session.query(User).where(User.id == body.user_id).first()
        if user is None:
            return abort(HTTPStatus.NOT_FOUND, "Пользователя с заданным id не существует.")
        question = db.session.query(Question).where(Question.id == body.test_question_id).first()
        if question is None:
            return abort(HTTPStatus.NOT_FOUND, "Вопроса с заданным id не существует.")
        progress_exists = (
            db.session.query(TestProgress)
            .where(
                TestProgress.user_id == body.user_id,
                TestProgress.test_question_id == body.test_question_id,
            )
            .first()
        )
        if progress_exists:
            return abort(HTTPStatus.CONFLICT, "Прогресс уже существует.")
        progress.from_dict(dict(body))
        db.session.add(progress)
        db.session.commit()
        return TestProgressBare.from_orm(progress)


class TestCompletedAPI(Resource):
    @validate()
    def get(self, completed_id: int) -> TestCompletedFull:
        """Получение данных определенного завершенного теста по id."""
        test_completed = TestCompleted.query.get(completed_id)
        if test_completed is None:
            return abort(HTTPStatus.NOT_FOUND, "Завершенных тестов с заданным id не существует.")
        return TestCompletedFull.from_orm(test_completed)

    @validate()
    def patch(self, completed_id: int, body: TestCompletedUpdate) -> TestCompletedFull:
        """Изменение данных определенного завершенного теста по id."""
        test_completed = TestCompleted.query.get(completed_id)
        if test_completed is None:
            return abort(HTTPStatus.NOT_FOUND, "Завершенного теста с заданным id не существует.")
        test_completed.from_dict(dict(body))
        db.session.commit()
        return TestCompletedFull.from_orm(test_completed)

    @validate()
    def delete(self, completed_id: int):
        """Блокировка завершенного теста."""
        test_completed = TestCompleted.query.get(completed_id)
        if test_completed is None:
            return abort(HTTPStatus.NOT_FOUND, "Завершенного теста с заданным id не существует.")
        if test_completed.deleted_at is not None:
            return abort(HTTPStatus.CONFLICT, "Результат уже заблокирован!")
        test_completed.deleted_at = datetime.utcnow()
        db.session.commit()
        return StatusResponse(warning="Результат заблокирован.")


class TestCompletedAPIList(Resource):
    @validate()
    def get(self, query: GetMultiQueryParams) -> TestCompletedList:
        """Получение списка завершенных тестов."""
        completed_tests_db = TestCompleted.query.all()
        test_data = [(dict(TestCompletedBare.from_orm(test))) for test in completed_tests_db]
        paginated_data = TestCompletedList.pagination(
            self, data=test_data, url="/api/v1/tests/completed/", query=query
        )
        return TestCompletedList(**paginated_data)

    @validate(on_success_status=HTTPStatus.CREATED)
    def post(self, body: TestCompletedCreate) -> TestCompletedBare:
        """Завершение теста."""
        test_completed = TestCompleted()
        user = db.session.query(User).where(User.id == body.user_id).first()
        if user is None:
            return abort(HTTPStatus.NOT_FOUND, "Пользователя с заданным id не существует.")
        test = db.session.query(Test).where(Test.id == body.test_id).first()
        if test is None:
            return abort(HTTPStatus.NOT_FOUND, "Теста с заданным id не существует.")
        test_completed_exists = (
            db.session.query(TestCompleted)
            .where(
                TestCompleted.user_id == body.user_id,
                TestCompleted.test_id == body.test_id,
            )
            .first()
        )
        if test_completed_exists:
            return abort(HTTPStatus.CONFLICT, "Тест уже пройден.")
        test_completed.from_dict(dict(body))
        db.session.add(test_completed)
        db.session.commit()
        return TestCompletedBare.from_orm(test_completed)
