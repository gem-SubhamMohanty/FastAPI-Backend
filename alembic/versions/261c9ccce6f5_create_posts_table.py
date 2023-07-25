"""create posts table

Revision ID: 261c9ccce6f5
Revises: 
Create Date: 2023-07-15 01:06:36.210546

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '261c9ccce6f5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key = True),sa.Column('title',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
