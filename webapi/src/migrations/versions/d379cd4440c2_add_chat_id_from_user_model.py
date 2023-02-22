"""add chat_id from user model

Revision ID: d379cd4440c2
Revises: 0656f5c8fb7a
Create Date: 2023-01-22 11:57:19.813487

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d379cd4440c2"
down_revision = "c04755e67cf6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("chat_id", sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "chat_id")
    # ### end Alembic commands ###
