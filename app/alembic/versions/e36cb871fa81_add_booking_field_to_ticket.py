"""add booking field to ticket

Revision ID: e36cb871fa81
Revises: dd9d051ca796
Create Date: 2020-11-13 08:31:09.765564

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e36cb871fa81'
down_revision = 'dd9d051ca796'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ticket', sa.Column('booking_token', sa.String(), nullable=True))
    op.add_column('ticket', sa.Column('date_search', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ticket', 'date_search')
    op.drop_column('ticket', 'booking_token')
    # ### end Alembic commands ###
