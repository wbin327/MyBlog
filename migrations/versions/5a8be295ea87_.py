"""empty message

Revision ID: 5a8be295ea87
Revises: 1ac27858950d
Create Date: 2018-02-17 14:39:52.282000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a8be295ea87'
down_revision = '1ac27858950d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('introduce', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'introduce')
    # ### end Alembic commands ###
