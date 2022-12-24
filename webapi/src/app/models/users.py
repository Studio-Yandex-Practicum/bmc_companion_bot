from app.models import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, Integer, SmallInteger, String


class User(BaseModel):
    """Модель пользователя."""

    __tablename__ = "users_users"

    first_name = Column("Имя", String(150))
    last_name = Column("Фамилия", String(150))
    middle_name = Column("Отчество", String(150))
    birthday = Column("Дата рождения", DateTime)
    phone = Column("Телефон пользователя", SmallInteger)
    telegram_id = Column("Id пользователя в телеграм", Integer)
    role_id = Column("Роль пользователя", Integer, ForeignKey("users_roles.id"), nullable=False)
    deleted_at = Column("Время удаления", DateTime)


class Role(BaseModel):
    """Роль пользователя."""

    __tablename__ = "users_roles"

    name = Column("Наименование роли", String(256), nullable=False)
