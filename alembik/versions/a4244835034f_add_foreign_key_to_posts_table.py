"""add foreign-key to posts table

Revision ID: a4244835034f
Revises: 06b030e3b138
Create Date: 2022-12-18 15:46:28.362690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4244835034f'
down_revision = '06b030e3b138'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_user_fk',source_table="posts",referent_table="users",
    local_cols=['owner_id'
                            ],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_user_fk',table_name="posts")
    op.drop_column('posts','owner_id')
    pass
