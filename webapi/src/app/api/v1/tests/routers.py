from datetime import datetime
from http import HTTPStatus

from app.db.pg import db
from app.models import Test
from app.schemas.core import GetMultiQueryParams, StatusResponse
from app.schemas.tests import TestCreate, TestList, TestResponse
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
