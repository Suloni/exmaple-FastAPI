"""add users table

Revision ID: 06b030e3b138
Revises: a96258201ed2
Create Date: 2022-12-18 15:14:53.541575

"""
from cgitb import text
from datetime import timezone
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06b030e3b138'
down_revision = 'a96258201ed2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
    sa.Column('id',sa.Integer(),nullable =False),
    sa.Column('email',sa.String(),nullable=False,unique=True),
    sa.Column('password',sa.String(),nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True), nullable=False,server_default=sa.text('now()')),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass
