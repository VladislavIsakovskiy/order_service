# flake8: noqa
"""create tables

Revision ID: e008bc4bcf82
Revises: 
Create Date: 2022-04-29 13:08:38.741094

"""
from alembic import op

import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e008bc4bcf82'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False, index=True),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("closed_at", sa.DateTime()),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "items",
        sa.Column("id", sa.Integer(), nullable=False, index=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String()),
        sa.Column("cost", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("available", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False, index=True),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("item_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["orders.id"],
        ),
        sa.ForeignKeyConstraint(
            ["item_id"],
            ["items.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("items")
    op.drop_table("orders")
    op.drop_table("order_items")
