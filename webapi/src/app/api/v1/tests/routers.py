from datetime import datetime
from http import HTTPStatus

from app.db.pg import db
from app.internal.api_services import test_completed_service, test_progress_service
from app.models import Test
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
        test_progress = test_progress_service.get_object_by_id(progress_id)
        return TestProgressFull.from_orm(test_progress)

    @validate()
    def patch(self, progress_id: int, body: TestProgressUpdate) -> TestProgressFull:
        """Изменение данных определенного прогресса по id."""
        progress = test_progress_service.progress_update(progress_id, body)
        return TestProgressFull.from_orm(progress)

    @validate()
    def delete(self, progress_id: int):
        """Блокировка прогресса пользователя."""
        test_progress_service.remove_object(progress_id)
        return StatusResponse(warning="Прогресс заблокирован.")


class TestProgressAPIList(Resource):
    @validate()
    def get(self, query: GetMultiQueryParams) -> TestProgressList:
        """Получение списка прогресса всех пользователей."""
        paginated_data = test_progress_service.get_paginated_objects_list(
            schema_singl_object=TestProgressBare,
            schema_list=TestProgressList,
            url="/api/v1/tests/progress/",
            query=query,
        )
        return TestProgressList(**paginated_data)

    @validate(on_success_status=HTTPStatus.CREATED)
    def post(self, body: TestProgressCreate) -> TestProgressBare:
        """Создание прогресса прохождения теста пользователем."""
        progress = test_progress_service.progress_create(body)
        return TestProgressBare.from_orm(progress)


class TestCompletedAPI(Resource):
    @validate()
    def get(self, completed_id: int) -> TestCompletedFull:
        """Получение данных определенного завершенного теста по id."""
        test_completed = test_completed_service.get_object_by_id(completed_id)
        return TestCompletedFull.from_orm(test_completed)

    @validate()
    def patch(self, completed_id: int, body: TestCompletedUpdate) -> TestCompletedFull:
        """Изменение данных определенного завершенного теста по id."""
        test_completed = test_completed_service.completed_update(completed_id, body)
        return TestCompletedFull.from_orm(test_completed)

    @validate()
    def delete(self, completed_id: int):
        """Блокировка завершенного теста."""
        test_completed_service.remove_object(completed_id)
        return StatusResponse(warning="Результат заблокирован.")


class TestCompletedAPIList(Resource):
    @validate()
    def get(self, query: GetMultiQueryParams) -> TestCompletedList:
        """Получение списка завершенных тестов."""
        paginated_data = test_completed_service.get_paginated_objects_list(
            schema_singl_object=TestCompletedBare,
            schema_list=TestCompletedList,
            url="/api/v1/tests/completed/",
            query=query,
        )
        return TestCompletedList(**paginated_data)

    @validate(on_success_status=HTTPStatus.CREATED)
    def post(self, body: TestCompletedCreate) -> TestCompletedBare:
        """Завершение теста."""
        test_completed = test_completed_service.completed_create(body)
        return TestCompletedBare.from_orm(test_completed)
