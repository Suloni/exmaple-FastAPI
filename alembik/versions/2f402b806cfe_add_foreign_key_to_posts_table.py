"""add foreign-key to posts table

Revision ID: 2f402b806cfe
Revises: a4244835034f
Create Date: 2022-12-18 18:28:22.582619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f402b806cfe'
down_revision = 'a4244835034f'
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
