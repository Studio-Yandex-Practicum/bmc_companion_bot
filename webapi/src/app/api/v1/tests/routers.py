from datetime import datetime
from http import HTTPStatus

from flask import abort
from flask_pydantic import validate
from flask_restful import Resource, fields

from app import pagination
from app.db.pg import db
from app.models import Test
from app.schemas.core import StatusResponse
from app.schemas.tests import TestCreate, TestResponse


DT_FORMAT = "%Y/%m/%d %H:%M:%S"


class TestAPI(Resource):

    @validate()
    def get(self, test_id) -> TestResponse:
        test = Test.query.get_or_404(test_id)
        if test.deleted_at is not None:
            return abort(HTTPStatus.NOT_FOUND, "Данный тест был удален!")
        return TestResponse.from_orm(test)

    @validate()
    def delete(self, test_id) -> StatusResponse:
        test = Test.query.get_or_404(test_id)
        test.deleted_at = datetime.utcnow().strftime(DT_FORMAT)
        db.session.commit()
        message = StatusResponse(
            warning="Ресурс заблокирован.",
        )
        return message


    @validate()
    def put(self, test_id, body: TestCreate) -> TestResponse:
        test = Test.query.get_or_404(test_id)
        if test.deleted_at is not None:
            return abort(HTTPStatus.NOT_FOUND, "Данный тест был удален!")
        test.from_dict(dict(body))
        test.updated_at = datetime.utcnow().strftime(DT_FORMAT)
        db.session.commit()
        return TestCreate.from_orm(test)


test_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'created_at': fields.DateTime(dt_format='iso8601'),
    'updated_at': fields.DateTime(dt_format='iso8601'),
    'deleted_at': fields.DateTime(dt_format='iso8601')
}


class TestAPIList(Resource):
    def get(self):
        test_db = Test.query.filter_by(deleted_at=None).all()
        return pagination.paginate(test_db, test_fields)

    @validate()
    def post(self, body: TestCreate) -> TestResponse:
        test = Test()
        test.from_dict(dict(body))
        db.session.add(test)
        db.session.commit()
        return TestResponse.from_orm(test)
