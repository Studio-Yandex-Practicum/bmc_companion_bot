from datetime import datetime
from http import HTTPStatus

from app.db.pg import db
from app.models import Role, User
from app.schemas.core import StatusResponse
from app.schemas.users import (
    GetMultiQueryParams,
    UserBare,
    UserCreate,
    UserFull,
    UserList,
    UserUpdate,
)
from flask import abort
from flask_pydantic import validate
from flask_restful import Resource


class ApiUserWithoutID(Resource):
    @validate()
    def get(self, query: GetMultiQueryParams) -> UserList:
        """Получение данных всех пользователей."""
        users = User.query.all()
        users_data = [(dict(UserBare.from_orm(user))) for user in users]
        paginated_data = UserList.pagination(self, users_data, query)
        return UserList(**paginated_data)

    @validate(on_success_status=HTTPStatus.CREATED)
    def post(self, body: UserCreate) -> UserFull:
        """Создание пользователя."""
        user = User()
        user_exists = db.session.query(User).where(User.phone == body.phone).first()
        if user_exists and body.phone is not None:
            return abort(HTTPStatus.CONFLICT, "Пользователь с таким номером телефона уже есть!")
        role = db.session.query(Role).where(Role.id == body.role_id).first()
        if role is None:
            return abort(HTTPStatus.NOT_FOUND, "Такой роли нет!")
        user.from_dict(dict(body))
        db.session.add(user)
        db.session.commit()
        return UserFull.from_orm(user)


class ApiUserWithID(Resource):
    @validate()
    def get(self, id: int) -> UserBare:
        """Получение данных определенного пользователя по id."""
        user = User.query.get(id)
        if user is None:
            return abort(HTTPStatus.NOT_FOUND, "Пользователя с заданным id не существует.")
        return UserFull.from_orm(user)

    @validate()
    def patch(self, id: int, body: UserUpdate) -> UserBare:
        """Изменение данных определенного пользователя по id."""
        user = User.query.get(id)
        if user is None:
            return abort(HTTPStatus.NOT_FOUND, "Пользователя с заданным id не существует.")
        phone_in_use = db.session.query(User).where(User.phone == body.phone).first()
        if phone_in_use and body.phone is not None:
            return abort(HTTPStatus.CONFLICT, "Пользователь с таким номером телефона уже есть!")
        role = db.session.query(Role).where(Role.id == body.role_id).first()
        if role is None:
            return abort(HTTPStatus.NOT_FOUND, "Такой роли нет!")
        user.from_dict(dict(body))
        db.session.commit()
        return UserBare.from_orm(user)

    @validate()
    def delete(self, id: int) -> StatusResponse:
        """Бан пользователя."""
        user = User.query.get(id)
        if user is None:
            return abort(HTTPStatus.NOT_FOUND, "Пользователя с заданным id не существует.")
        if user.deleted_at is not None:
            return abort(HTTPStatus.CONFLICT, "Пользоваетель уже забанен!")
        user.deleted_at = datetime.utcnow()
        db.session.commit()
        return StatusResponse(message="Пользоваетель забанен.")
