"""announce

Revision ID: 04f714a52f35
Revises: 323629b28746
Create Date: 2023-05-23 01:31:40.446754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "04f714a52f35"
down_revision = "323629b28746"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "announcements",
        sa.Column("statement", sa.String(), nullable=False),
        sa.Column("by", sa.Integer(), nullable=False),
        sa.Column("at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("announcements")
    # ### end Alembic commands ###