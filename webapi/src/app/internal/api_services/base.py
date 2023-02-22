from datetime import datetime
from http import HTTPStatus

from app.internal.model_services import BaseModelService
from flask import abort


class BaseAPIService:
    def __init__(self, model):
        self.model = model
        self.service = BaseModelService(self.model)

    def get_object_by_id(self, id: int):
        db_object = self.service.get_object_or_none(self, id)
        if db_object is None:
            return abort(HTTPStatus.NOT_FOUND, "Объекта с заданным id не существует.")
        return db_object

    def get_paginated_objects_list(self, schema_singl_object, schema_list, url, query):
        db_objects = self.service.get_all_objects(self)
        db_objects_data = [(dict(schema_singl_object.from_orm(object))) for object in db_objects]
        paginated_data = schema_list.pagination(self, data=db_objects_data, url=url, query=query)
        return paginated_data

    def remove_object(self, id: int):
        db_object = self.service.get_object_or_none(self, id)
        if db_object is None:
            return abort(HTTPStatus.NOT_FOUND, "Объекта с заданным id не существует.")
        if db_object.deleted_at is not None:
            return abort(HTTPStatus.CONFLICT, "Объект уже заблокирован!")
        db_object.deleted_at = datetime.utcnow()
        self.service.update(self)
