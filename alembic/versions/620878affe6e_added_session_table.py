"""added session table

Revision ID: 620878affe6e
Revises: 825944411f8d
Create Date: 2025-02-26 11:29:38.224461

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '620878affe6e'
down_revision: Union[str, None] = '825944411f8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
