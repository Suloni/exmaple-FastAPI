"""create posts table

Revision ID: bdef8a3d388d
Revises: 
Create Date: 2022-12-17 12:41:34.384982

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bdef8a3d388d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),sa.Column(
        'title',sa.String(),nullable=False)
        ,sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_table('posts')

    pass
