"""empty message

Revision ID: 8db176334500
Revises: 5bff758229f4
Create Date: 2021-04-29 10:17:51.762261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8db176334500'
down_revision = '5bff758229f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questions', sa.Column('file_path', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('questions', 'file_path')
    # ### end Alembic commands ###
