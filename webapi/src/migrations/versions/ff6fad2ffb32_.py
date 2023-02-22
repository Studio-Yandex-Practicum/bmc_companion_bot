"""empty message

Revision ID: ff6fad2ffb32
Revises: d379cd4440c2
Create Date: 2023-01-28 19:12:39.491527

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ff6fad2ffb32"
down_revision = "d379cd4440c2"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("telegram_login", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "telegram_login")
    # ### end Alembic commands ###
