from app.models import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, Integer, SmallInteger, String


class User(BaseModel):
    """Модель пользователя."""

    __tablename__ = "users"
    __table_args__ = {"schema": "general"}

    first_name = Column("Имя", String(150))
    last_name = Column("Фамилия", String(150))
    middle_name = Column("Отчество", String(150))
    birthday = Column("Дата рождения", DateTime)
    phone = Column("Телефон пользователя", SmallInteger)
    telegram_id = Column("Id пользователя в телеграм", Integer)
    role_id = Column("Роль пользователя", Integer, ForeignKey("general.roles.id"), nullable=False)
    deleted_at = Column("Время удаления", DateTime)

    def to_dict(self):
        return dict(
            first_name=self.first_name,
            last_name=self.last_name,
            middle_name=self.middle_name,
            birthday=self.birthday,
            phone=self.phone,
            telegram_id=self.telegram_id,
            role_id=self.role_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at,
        )

    def from_dict(self, data):
        for key, item in data.items():
            setattr(self, key, item)


class Role(BaseModel):
    """Роль пользователя."""

    __tablename__ = "roles"
    __table_args__ = {"schema": "general"}

    name = Column("Наименование роли", String(256), nullable=False)
