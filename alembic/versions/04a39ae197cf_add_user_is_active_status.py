"""add user is_active status

Revision ID: 04a39ae197cf
Revises: 967b8abfaf97
Create Date: 2024-04-08 13:18:36.217225

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "04a39ae197cf"
down_revision: Union[str, None] = "967b8abfaf97"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column("is_active", sa.Boolean(), server_default="0", nullable=False),
    )
    op.alter_column(
        "users",
        "password",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=15),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users",
        "password",
        existing_type=sa.String(length=15),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
    op.drop_column("users", "is_active")
    # ### end Alembic commands ###
