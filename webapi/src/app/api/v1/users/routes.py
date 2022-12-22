from datetime import datetime
from http import HTTPStatus

from app.db.pg import db
from app.models import Role, User
from app.schemas.users import UserCreate, UserDB
from flask import abort
from flask_pydantic import validate
from flask_restful import Resource


class UserApiCreate(Resource):
    @validate(on_success_status=HTTPStatus.CREATED)
    def post(self, body: UserCreate) -> UserDB:
        user = User()
        user_exists = db.session.query(User).where(User.phone == body.phone).first()
        if user_exists and body.phone is not None:
            return abort(HTTPStatus.CONFLICT, "Пользователь с таким номером телефона уже есть!")
        role_exists = db.session.query(Role).where(Role.id == body.role_id).first()
        if role_exists:
            user.from_dict(dict(body))
            db.session.add(user)
            db.session.commit()
            return UserDB.from_orm(user)
        return abort(HTTPStatus.CONFLICT, "Такой роли нет!")

    @validate()
    def get(self, id) -> UserDB:
        user = User.query.get_or_404(id)
        return UserDB.from_orm(user)

    @validate()
    def patch(self, id, body: UserCreate) -> UserDB:
        user = User.query.get_or_404(id)
        phone_in_use = db.session.query(User).where(User.phone == body.phone).first()
        if phone_in_use and body.phone is not None:
            return abort(HTTPStatus.CONFLICT, "Пользователь с таким номером телефона уже есть!")
        role_exists = db.session.query(Role).where(Role.id == body.role_id).first()
        if role_exists:
            user.from_dict(dict(body))
            db.session.commit()
            return UserDB.from_orm(user)
        return abort(HTTPStatus.CONFLICT, "Такой роли нет!")

    @validate()
    def delete(self, id):
        user = User.query.get_or_404(id)
        user.deleted_at = datetime.utcnow()
        db.session.commit()
        return {"message": "Пользоваетель забанен."}


def register_router(api):
    api.add_resource(UserApiCreate, "/api/v1/users", "/api/v1/users/<int:id>")
