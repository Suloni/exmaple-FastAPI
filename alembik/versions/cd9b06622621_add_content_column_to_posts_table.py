"""add content column to posts table

Revision ID: cd9b06622621
Revises: bdef8a3d388d
Create Date: 2022-12-18 13:35:15.203014

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd9b06622621'
down_revision = 'bdef8a3d388d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass

