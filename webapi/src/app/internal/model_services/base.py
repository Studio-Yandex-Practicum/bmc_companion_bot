from typing import TypeVar

from app.db.pg import db

DataBaseModel = TypeVar("DataBaseModel")


class BaseModelService:
    """Базовый класс для работы с моделями."""

    def __init__(self, model):
        self.model = model

    def get_object_or_none(self, id: int):
        db_object = self.model.query.filter_by(id=id).first()
        return db_object

    def get_all_objects(self):
        db_objects = self.model.query.all()
        return db_objects

    def create(self, data: DataBaseModel):
        db.session.add(data)
        db.session.commit()
        return data

    def update(self):
        db.session.commit()
