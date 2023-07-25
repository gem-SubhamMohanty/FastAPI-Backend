"""add user_reg table

Revision ID: bb034be17571
Revises: eafaaee79f34
Create Date: 2023-07-15 09:18:55.105045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb034be17571'
down_revision = 'eafaaee79f34'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user_reg',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('user_reg')
    pass
