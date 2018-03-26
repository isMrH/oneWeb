"""empty message

Revision ID: bbace36c99e7
Revises: 
Create Date: 2018-01-19 10:13:44.948381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbace36c99e7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('navigation',
    sa.Column('navId', sa.Integer(), nullable=False),
    sa.Column('navName', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('navId')
    )
    op.create_table('menu',
    sa.Column('mId', sa.Integer(), nullable=False),
    sa.Column('mName', sa.String(length=20), nullable=True),
    sa.Column('link', sa.String(length=50), nullable=True),
    sa.Column('navId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['navId'], ['navigation.navId'], ),
    sa.PrimaryKeyConstraint('mId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('menu')
    op.drop_table('navigation')
    # ### end Alembic commands ###