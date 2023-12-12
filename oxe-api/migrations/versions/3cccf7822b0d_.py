"""empty message

Revision ID: 3cccf7822b0d
Revises: 7855a5f3f5f1
Create Date: 2023-10-12 22:35:48.958133

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "3cccf7822b0d"
down_revision = "7855a5f3f5f1"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "Document",
        sa.Column(
            "is_private",
            mysql.TINYINT(display_width=1),
            server_default=sa.text("'0'"),
            autoincrement=False,
            nullable=True,
        ),
    )


def downgrade():
    op.drop_column('Document', 'private')
