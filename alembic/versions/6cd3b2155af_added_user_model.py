"""Added User Model

Revision ID: 6cd3b2155af
Revises:
Create Date: 2015-07-30 17:36:52.799115

"""

# revision identifiers, used by Alembic.
revision = '6cd3b2155af'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.Unicode(length=40), nullable=False),
        sa.Column('last_name', sa.Unicode(length=40), nullable=False),
        sa.Column('username', sa.Unicode(length=40), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=True),
        sa.Column('last_login', sqlalchemy_utils.types.arrow.ArrowType(), nullable=True),
        sa.Column('created_at', sqlalchemy_utils.types.arrow.ArrowType(), nullable=False),
        sa.Column('updated_at', sqlalchemy_utils.types.arrow.ArrowType(), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
        sa.UniqueConstraint('email', name=op.f('uq_users_email')),
        sa.UniqueConstraint('username', name=op.f('uq_users_username'))
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    ### end Alembic commands ###