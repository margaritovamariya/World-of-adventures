"""Add recommended

Revision ID: 22cd6f808509
Revises: 3b7893cee8b4
Create Date: 2024-12-29 23:33:42.513962

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22cd6f808509'
down_revision = '3b7893cee8b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('recommended', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('recommended')

    # ### end Alembic commands ###