from datetime import datetime
from http import HTTPStatus

from app.db.pg import db
from app.models import QuestionType
from app.schemas.core import StatusResponse
from app.schemas.questions import QuestionCreate, QuestionDB, QuestionUpdate
from flask import Flask, abort
from flask_pydantic import validate
from flask_rest_paginate import Pagination
from flask_restful import Resource, fields

FORMAT = "%Y/%m/%d %H:%M:%S"

app = Flask(__name__)

pagination = Pagination(app, db)


class QuestionTypeApi(Resource):
    @validate(on_success_status=HTTPStatus.CREATED)
    def post(self, body: QuestionCreate) -> QuestionDB:
        question_type = QuestionType()
        question_type_exists = (
            db.session.query(QuestionType).where(QuestionType.name == body.name).first()
        )
        if question_type_exists is not None:
            return abort(HTTPStatus.CONFLICT, "Такой тип вопроса уже есть!")

        question_type.from_dict(dict(body))
        db.session.add(question_type)
        question_type.created_at = datetime.utcnow().strftime(FORMAT)
        db.session.commit()
        return QuestionDB.from_orm(question_type)

    @validate()
    def get(self, id: int) -> QuestionDB:
        question_type = QuestionType.query.get_or_404(id)
        return QuestionDB.from_orm(question_type)

    @validate()
    def patch(self, id: int, body: QuestionUpdate) -> QuestionDB:
        question_type = QuestionType.query.get_or_404(id)
        question_type_exists = (
            db.session.query(QuestionType).where(QuestionType.name == body.name).first()
        )
        if question_type_exists is not None:
            return abort(HTTPStatus.CONFLICT, "Такой тип вопроса уже есть!")
        question_type.from_dict(dict(body))
        question_type.updated_at = datetime.utcnow().strftime(FORMAT)
        db.session.commit()
        return QuestionDB.from_orm(question_type)

    @validate()
    def delete(self, id: int) -> StatusResponse:
        question_type = QuestionType.query.get_or_404(id)
        question_type.deleted_at = datetime.utcnow().strftime(FORMAT)
        db.session.commit()
        message = StatusResponse(
            warning="Ресурс заблокирован.",
        )
        return message


test_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "validation_regexp": fields.String,
    "created_at": fields.DateTime(dt_format="iso8601"),
    "updated_at": fields.DateTime(dt_format="iso8601"),
}


class QuestionTypeAPIList(Resource):
    @validate()
    def get(self):
        question_type_db = QuestionType.query.filter_by(deleted_at=None).all()
        return pagination.paginate(question_type_db, test_fields)


def register_router(api):
    api.add_resource(QuestionTypeAPIList, "/api/v1/questions/")
    api.add_resource(QuestionTypeApi, "/api/v1/questions", "/api/v1/questions/<int:id>")
