"""added about author field

Revision ID: 81369569a817
Revises: d6276872c785
Create Date: 2022-11-13 19:02:24.767303

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81369569a817'
down_revision = 'd6276872c785'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('about_author', sa.Text(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'about_author')
    # ### end Alembic commands ###