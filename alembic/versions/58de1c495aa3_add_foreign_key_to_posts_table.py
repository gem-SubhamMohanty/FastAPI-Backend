"""add foreign key to posts table

Revision ID: 58de1c495aa3
Revises: bb034be17571
Create Date: 2023-07-15 09:25:58.735332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58de1c495aa3'
down_revision = 'bb034be17571'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
         'owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="user_reg", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
