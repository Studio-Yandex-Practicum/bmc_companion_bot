"""Add model Answer

Revision ID: 0656f5c8fb7a
Revises: 8d9e9f4ffac9
Create Date: 2023-01-16 15:51:53.939578

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0656f5c8fb7a"
down_revision = "8d9e9f4ffac9"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "answers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("text", sa.Text(), nullable=True),
        sa.Column("question_id", sa.Integer(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True, comment="Время удаления"),
        sa.ForeignKeyConstraint(
            ["question_id"],
            ["questions.id"],
            name=op.f("fk_answers_question_id_questions"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_answers")),
    )
    op.add_column("completed_tests", sa.Column("answer_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        op.f("fk_completed_tests_answer_id_answers"),
        "completed_tests",
        "answers",
        ["answer_id"],
        ["id"],
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        op.f("fk_completed_tests_answer_id_answers"), "completed_tests", type_="foreignkey"
    )
    op.drop_column("completed_tests", "answer_id")
    op.drop_table("answers")
    # ### end Alembic commands ###
