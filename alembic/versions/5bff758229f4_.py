"""empty message

Revision ID: 5bff758229f4
Revises: 4ccd7d4db816
Create Date: 2021-04-11 13:07:56.733710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bff758229f4'
down_revision = '4ccd7d4db816'
branch_labels = None
depends_on = None
from sqlalchemy.dialects import postgresql


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    feedback_state = postgresql.ENUM('PENDING', 'PASSED', 'FIXED', 'BROKEN', 'FAILED', 'STILL_FAILING', 'CANCELED', 'ERRORED', name='feedbackstate')
    feedback_state.create(op.get_bind())
    op.add_column('feedbacks', sa.Column('state', sa.Enum('PENDING', 'PASSED', 'FIXED', 'BROKEN', 'FAILED', 'STILL_FAILING', 'CANCELED', 'ERRORED', name='feedbackstate'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('feedbacks', 'state')
    # ### end Alembic commands ###