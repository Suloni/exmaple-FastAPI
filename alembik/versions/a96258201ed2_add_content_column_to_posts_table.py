"""add content column to posts table

Revision ID: a96258201ed2
Revises: cd9b06622621
Create Date: 2022-12-18 13:36:41.680283

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a96258201ed2'
down_revision = 'cd9b06622621'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
