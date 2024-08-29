"""Initial migration

Revision ID: 59e32fa61739
Revises: 
Create Date: 2024-08-26 19:43:56.385071

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '59e32fa61739'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('orders',sa.Column('locker',sa.String))
    op.add_column('orders',sa.Column('full_name',sa.String))
    op.add_column('orders',sa.Column('phone_number',sa.String))
    op.add_column('orders',sa.Column('city',sa.String))
    op.add_column('orders',sa.Column('status',sa.String))
    op.add_column('orders',sa.Column('address',sa.String))
    op.add_column('orders',sa.Column('payment_method',sa.String))


def downgrade() -> None:
    pass
