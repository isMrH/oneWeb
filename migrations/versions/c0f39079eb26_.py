"""empty message

Revision ID: c0f39079eb26
Revises: bbace36c99e7
Create Date: 2018-01-20 18:50:53.654180

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0f39079eb26'
down_revision = 'bbace36c99e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('article',
    sa.Column('aId', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('src', sa.String(length=50), nullable=True),
    sa.Column('mId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['mId'], ['menu.mId'], ),
    sa.PrimaryKeyConstraint('aId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('article')
    # ### end Alembic commands ###
