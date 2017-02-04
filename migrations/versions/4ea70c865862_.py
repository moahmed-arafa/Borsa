"""empty message

Revision ID: 4ea70c865862
Revises: dd254f74c8b7
Create Date: 2017-02-04 11:30:27.267769

"""

# revision identifiers, used by Alembic.
revision = '4ea70c865862'
down_revision = 'dd254f74c8b7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('company', sa.Column('name_ar', sa.String(), nullable=True))
    op.add_column('company', sa.Column('symbol', sa.String(), nullable=True))
    op.add_column('company', sa.Column('website', sa.String(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('company', 'website')
    op.drop_column('company', 'symbol')
    op.drop_column('company', 'name_ar')
    ### end Alembic commands ###
