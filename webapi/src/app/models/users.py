from app import db
from app.models import BaseModel

user_role_association = db.Table(
    "users_roles_associations",
    db.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("user_roles_id", db.Integer, db.ForeignKey("user_roles.id"), primary_key=True),
)


class User(BaseModel):
    """Модель пользователя."""

    __tablename__ = "users"

    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    middle_name = db.Column(db.String(150))
    birthday = db.Column(db.DateTime)
    phone = db.Column(db.SmallInteger)
    roles = db.relationship("UserRole", secondary=user_role_association, backref="users")
    telegram_id = db.Column(db.Integer)
    deleted_at = db.Column(db.DateTime)


class UserRole(BaseModel):
    """Роль пользователя."""

    __tablename__ = "user_roles"

    name = db.Column(db.String(256), unique=True, nullable=False)

    def __repr__(self):
        return f"<Role {self.name}>"
