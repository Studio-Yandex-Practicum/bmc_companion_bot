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
    deleted_at = db.Column(db.DateTime)


class UserRole(BaseModel):
    """Роль пользователя."""

    __tablename__ = "user_roles"

    name = db.Column(db.String(256), unique=True, nullable=False)
    users = db.relationship("User")

    def __repr__(self):
        return f"<Role {self.name}>"
