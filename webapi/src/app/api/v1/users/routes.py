from datetime import datetime
from http import HTTPStatus
from typing import List

from app.core.exceptions import (
    PhoneAlreadyExists,
    RoleNotExists,
    UserAlreadyBanned,
    UserNotExists,
)
from app.db.pg import db
from app.models import Role, User
from app.schemas.core import StatusResponse
from app.schemas.users import UserBare, UserCreate, UserFull, UserList, UserUpdate
from flask import jsonify
from flask_pydantic import validate
from flask_restful import Resource


class ApiUserWithoutID(Resource):
    @validate()
    def get(self) -> List[UserList]:
        """Получение данных всех пользователей."""
        users = User.query.all()
        users_data = [dict(UserList.from_orm(user)) for user in users]
        # return jsonify(
        #     get_paginated_list(
        #         users_data,
        #         "/api/v1/users",
        #         start=request.args.get("start", 1),
        #         limit=request.args.get("limit", 10),
        #     )
        # )
        return jsonify(users_data)

    @validate(on_success_status=HTTPStatus.CREATED)
    def post(self, body: UserCreate) -> UserFull:
        """Создание пользователя."""
        user = User()
        user_exists = db.session.query(User).where(User.phone == body.phone).first()
        if user_exists and body.phone is not None:
            raise PhoneAlreadyExists
        role = db.session.query(Role).where(Role.id == body.role_id).first()
        if role is None:
            raise RoleNotExists
        user.from_dict(dict(body))
        db.session.add(user)
        db.session.commit()
        return UserFull.from_orm(user)


class ApiUserWithID(Resource):
    @validate()
    def get(self, id) -> UserBare:
        """Получение данных определенного пользователя по id."""
        user = User.query.get(id)
        if user is None:
            raise UserNotExists
        return UserFull.from_orm(user)

    @validate()
    def patch(self, id, body: UserUpdate) -> UserBare:
        """Изменение данных определенного пользователя по id."""
        user = User.query.get(id)
        if user is None:
            raise UserNotExists
        phone_in_use = db.session.query(User).where(User.phone == body.phone).first()
        if phone_in_use and body.phone is not None:
            raise PhoneAlreadyExists
        role = db.session.query(Role).where(Role.id == body.role_id).first()
        if role is None:
            raise RoleNotExists
        user.from_dict(dict(body))
        db.session.commit()
        return UserBare.from_orm(user)

    @validate()
    def delete(self, id):
        """Бан пользователя."""
        user = User.query.get(id)
        if user is None:
            raise UserNotExists
        if user.deleted_at is not None:
            raise UserAlreadyBanned
        user.deleted_at = datetime.utcnow()
        db.session.commit()
        return StatusResponse(message="Пользоваетель забанен.")
