"""empty message

Revision ID: b41151588ad0
Revises: 437948555897
Create Date: 2021-04-03 10:57:14.859663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b41151588ad0'
down_revision = '437948555897'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles_to_users',
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.alter_column('submissions', 'purpose',
               existing_type=sa.VARCHAR(length=15),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('submissions', 'purpose',
               existing_type=sa.VARCHAR(length=15),
               nullable=True)
    op.drop_table('roles_to_users')
    # ### end Alembic commands ###
