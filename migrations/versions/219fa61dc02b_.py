"""empty message

Revision ID: 219fa61dc02b
Revises: 13c27ab7e61e
Create Date: 2015-06-23 20:39:18.106744

"""

# revision identifiers, used by Alembic.
revision = '219fa61dc02b'
down_revision = '13c27ab7e61e'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('events', 'location_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('events', 'location_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    ### end Alembic commands ###