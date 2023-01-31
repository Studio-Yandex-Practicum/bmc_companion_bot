from app import db
from app.models import BaseModel


class User(BaseModel):
    """Модель пользователя."""

    __tablename__ = "users"

    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    middle_name = db.Column(db.String(150))
    birthday = db.Column(db.DateTime)
    phone = db.Column(db.SmallInteger)
    role_id = db.Column(db.Integer, db.ForeignKey("user_roles.id"), nullable=False)
    telegram_id = db.Column(db.Integer)
    telegram_login = db.Column(db.String)
    chat_id = db.Column(db.Integer)
    deleted_at = db.Column(db.DateTime)

    def to_dict(self):
        return dict(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            middle_name=self.middle_name,
            birthday=self.birthday,
            phone=self.phone,
            role_id=self.role_id,
            telegram_id=self.telegram_id,
            telegram_login=self.telegram_login,
            chat_id=self.chat_id,
            deleted_at=self.deleted_at,
        )


class UserRole(BaseModel):
    """Роль пользователя."""

    __tablename__ = "user_roles"

    name = db.Column(db.String(256), unique=True, nullable=False)
    users = db.relationship("User")

    def __repr__(self):
        return f"<Role {self.name}>"
