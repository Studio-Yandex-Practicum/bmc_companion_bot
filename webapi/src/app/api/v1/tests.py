from datetime import datetime

from app.models.tests import Test, db
from app.schemas.tests import TestCreate, TestDB
from flask import Flask
from flask_pydantic import validate
from flask_rest_paginate import Pagination
from flask_restful import Api, Resource, fields

app = Flask(__name__)
api = Api(app)
pagination = Pagination(app, db)


class TestAPI(Resource):

    @validate()
    def get(self, test_id) -> TestDB:
        test = Test.query.get_or_404(test_id)
        if test.deleted_at is not None:
            return {'status': 404, 'message': 'Данный тест был удален'}
        return TestDB.from_orm(test)

    @validate()
    def delete(self, test_id):
        test = Test.query.get_or_404(test_id)
        test.deleted_at = datetime.utcnow()
        db.session.commit()
        return {'status': 204, 'message': 'Тест успешно удален'}

    @validate()
    def put(self, test_id, body: TestCreate) -> TestDB:
        test = Test.query.get_or_404(test_id)
        if test.deleted_at is not None:
            return {'status': 404, 'message': 'Данный тест был удален'}
        test.from_dict(dict(body))
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
    def post(self, body: TestCreate) -> TestDB:
        test = Test()
        test.from_dict(dict(body))
        db.session.add(test)
        db.session.commit()
        return TestDB.from_orm(test)


api.add_resource(TestAPIList, '/api/tests/')
api.add_resource(TestAPI, '/api/tests/<int:test_id>/')
