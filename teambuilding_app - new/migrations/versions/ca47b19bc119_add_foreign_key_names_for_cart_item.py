"""Add foreign key names for cart_item

Revision ID: ca47b19bc119
Revises: 22cd6f808509
Create Date: 2025-01-01 23:08:00.648080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca47b19bc119'
down_revision = '22cd6f808509'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cart_item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('tracking_id', sa.String(), nullable=True))
        batch_op.create_foreign_key('fk_cartitem_user_id', 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cart_item', schema=None) as batch_op:
        batch_op.drop_constraint('fk_cartitem_user_id', type_='foreignkey')
        batch_op.drop_column('tracking_id')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###