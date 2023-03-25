"""Add users table

Revision ID: 569ead36c55d
Revises: bddbbb066c16
Create Date: 2023-03-24 21:45:28.293464

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "569ead36c55d"
down_revision = "bddbbb066c16"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("about", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "last_login", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "last_login_id_name_index",
        "users",
        ["last_login", "id", "name"],
        unique=False,
        postgresql_ops={"name": "DESC"},
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        "last_login_id_name_index", table_name="users", postgresql_ops={"name": "DESC"}
    )
    op.drop_table("users")
    # ### end Alembic commands ###