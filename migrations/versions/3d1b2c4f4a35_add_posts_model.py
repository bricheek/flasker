"""add posts model

Revision ID: 3d1b2c4f4a35
Revises: 8270c2683449
Create Date: 2022-11-10 22:14:28.520619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d1b2c4f4a35'
down_revision = '8270c2683449'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('author', sa.String(length=255), nullable=True),
    sa.Column('date_posted', sa.DateTime(), nullable=True),
    sa.Column('slug', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    # ### end Alembic commands ###
