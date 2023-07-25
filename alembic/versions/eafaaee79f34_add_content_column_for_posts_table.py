"""add content column for posts table

Revision ID: eafaaee79f34
Revises: 261c9ccce6f5
Create Date: 2023-07-15 09:13:25.616892

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eafaaee79f34'
down_revision = '261c9ccce6f5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
