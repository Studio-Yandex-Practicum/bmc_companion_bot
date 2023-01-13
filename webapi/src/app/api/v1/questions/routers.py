from datetime import datetime
from http import HTTPStatus

from app.db.pg import db
from app.models import Question, QuestionType
from app.schemas.core import GetMultiQueryParams, StatusResponse
from app.schemas.questions import (
    QuestionCreate,
    QuestionList,
    QuestionResponse,
    QuestionTypeCreate,
    QuestionTypeList,
    QuestionTypeResponse,
    QuestionTypeResponseMini,
    QuestionTypeUpdate,
    QuestionUpdate,
)
from flask import abort
from flask_pydantic import validate
from flask_restful import Resource

FORMAT = "%Y/%m/%d %H:%M:%S"


class QuetionAPI(Resource):
    @validate()
    def get(self, id: int) -> QuestionResponse:
        """Получение данных вопроса по id."""
        question = Question.query.get(id)
        if question is None:
            return abort(HTTPStatus.NOT_FOUND, "Вопроса с заданным id не существует.")
        return QuestionResponse.from_orm(question)

    @validate()
    def patch(self, id: int, body: QuestionUpdate) -> QuestionResponse:
        """Изменение данных определенного вопроса по id."""
        question = Question.query.get(id)
        if question is None:
            return abort(HTTPStatus.NOT_FOUND, "Вопроса с заданным id не существует.")
        if question.deleted_at is not None:
            return abort(HTTPStatus.NOT_FOUND, "Вопрос с заданным id заблокирован.")
        question_exists = db.session.query(Question).where(Question.text == body.text).first()
        if question_exists is not None:
            return abort(HTTPStatus.CONFLICT, "Такой вопрос уже есть!")
        question.from_dict(dict(body))
        question.updated_at = datetime.utcnow().strftime(FORMAT)
        db.session.commit()
        return QuestionResponse.from_orm(question)

    @validate()
    def delete(self, id: int) -> StatusResponse:
        """Soft-delete вопроса."""
        question = Question.query.get(id)
        if question is None:
            return abort(HTTPStatus.NOT_FOUND, "Вопроса с заданным id не существует.")
        if question.deleted_at is not None:
            return abort(HTTPStatus.CONFLICT, "Вопрос уже заблокирован!")
        question.deleted_at = datetime.utcnow().strftime(FORMAT)
        db.session.commit()
        message = StatusResponse(
            warning="Ресурс заблокирован.",
        )
        return message


class QuestionAPIList(Resource):
    @validate(on_success_status=HTTPStatus.CREATED)
    def post(self, body: QuestionCreate) -> QuestionResponse:
        """Создание вопроса."""
        question = Question()
        question_exists = db.session.query(Question).where(Question.text == body.text).first()
        if question_exists is not None:
            return abort(HTTPStatus.CONFLICT, "Такой вопрос уже есть!")
        question.from_dict(dict(body))
        db.session.add(question)
        question.created_at = datetime.utcnow().strftime(FORMAT)
        db.session.commit()
        return QuestionResponse.from_orm(question)

    @validate()
    def get(self, query: GetMultiQueryParams) -> QuestionList:
        """Получение данных всех вопросов."""
        question_db = Question.query.filter_by(deleted_at=None).all()
        question_data = [(dict(QuestionResponse.from_orm(question))) for question in question_db]
        paginated_data = QuestionList.pagination(
            self, data=question_data, url="/api/v1/questions/", query=query
        )
        return QuestionList(**paginated_data)


class QuestionTypeAPI(Resource):
    @validate()
    def get(self, id: int) -> QuestionTypeResponse:
        """Получение данных типа вопроса по id."""
        question_type = QuestionType.query.get(id)
        if question_type is None:
            return abort(HTTPStatus.NOT_FOUND, "Тип вопроса с заданным id не существует.")
        return QuestionTypeResponse.from_orm(question_type)

    @validate()
    def patch(self, id: int, body: QuestionTypeUpdate) -> QuestionTypeResponse:
        """Изменение данных определенного типа вопроса по id."""
        question_type = QuestionType.query.get(id)
        if question_type is None:
            return abort(HTTPStatus.NOT_FOUND, "Типа вопроса с заданным id не существует.")
        question_type_exists = (
            db.session.query(QuestionType).where(QuestionType.name == body.name).first()
        )
        if question_type_exists is not None:
            return abort(HTTPStatus.CONFLICT, "Такой тип вопроса уже есть!")
        question_type.from_dict(dict(body))
        question_type.updated_at = datetime.utcnow().strftime(FORMAT)
        db.session.commit()
        return QuestionTypeResponse.from_orm(question_type)

    @validate()
    def delete(self, id: int) -> StatusResponse:
        """Soft-delete типа вопроса."""
        question_type = QuestionType.query.get(id)
        if question_type is None:
            return abort(HTTPStatus.NOT_FOUND, "Типа вопроса с заданным id не существует.")
        if question_type.deleted_at is not None:
            return abort(HTTPStatus.CONFLICT, "Тип вопроса уже заблокирован!")
        question_type.deleted_at = datetime.utcnow().strftime(FORMAT)
        db.session.commit()
        message = StatusResponse(
            warning="Ресурс заблокирован.",
        )
        return message


class QuestionTypeAPIList(Resource):
    @validate(on_success_status=HTTPStatus.CREATED)
    def post(self, body: QuestionTypeCreate) -> QuestionTypeResponse:
        """Создание типа вопроса."""
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
        return QuestionTypeResponse.from_orm(question_type)

    @validate()
    def get(self, query: GetMultiQueryParams) -> QuestionTypeList:
        """Получение данных всех типов вопросов."""
        question_type_db = QuestionType.query.filter_by(deleted_at=None).all()
        question_type_data = [
            (dict(QuestionTypeResponseMini.from_orm(question_type)))
            for question_type in question_type_db
        ]
        paginated_data = QuestionTypeList.pagination(
            self, data=question_type_data, url="/api/v1/question-type/", query=query
        )
        return QuestionTypeList(**paginated_data)
