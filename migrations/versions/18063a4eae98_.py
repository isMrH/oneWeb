"""empty message

Revision ID: 18063a4eae98
Revises: edf9e6d0b501
Create Date: 2018-02-11 21:50:05.710485

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18063a4eae98'
down_revision = 'edf9e6d0b501'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('uId', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('uId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###