from http import HTTPStatus

from app.internal.api_services import user_service
from app.schemas.core import GetMultiQueryParams, StatusResponse
from app.schemas.users import UserBare, UserCreate, UserFull, UserList, UserUpdate
from flask_pydantic import validate
from flask_restful import Resource


class ApiUserWithoutID(Resource):
    @validate()
    def get(self, query: GetMultiQueryParams) -> UserList:
        """Получение данных всех пользователей."""
        paginated_data = user_service.get_paginated_objects_list(
            schema_singl_object=UserBare,
            schema_list=UserList,
            url="/api/v1/users/",
            query=query,
        )
        return UserList(**paginated_data)

    @validate(on_success_status=HTTPStatus.CREATED)
    def post(self, body: UserCreate) -> UserFull:
        """Создание пользователя."""
        user = user_service.user_create(body)
        return UserFull.from_orm(user)


class ApiUserWithID(Resource):
    @validate()
    def get(self, id: int) -> UserBare:
        """Получение данных определенного пользователя по id."""
        user = user_service.get_object_by_id(id)
        return UserFull.from_orm(user)

    @validate()
    def patch(self, id: int, body: UserUpdate) -> UserBare:
        """Изменение данных определенного пользователя по id."""
        user = user_service.user_update(id, body)
        return UserBare.from_orm(user)

    @validate()
    def delete(self, id: int) -> StatusResponse:
        """Бан пользователя."""
        user_service.remove_object(id)
        return StatusResponse(warning="Пользоваетель забанен.")
