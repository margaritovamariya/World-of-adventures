"""empty message

Revision ID: 3b7893cee8b4
Revises: 
Create Date: 2024-12-27 01:05:33.119524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b7893cee8b4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            constraint_name='fk_product_category',  # Добавено име на ограничението
            referent_table='category',
            local_cols=['category_id'],
            remote_cols=['id']
        )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_constraint('fk_product_category', type_='foreignkey')  # Използваме същото име за премахване
        batch_op.drop_column('category_id')
    # ### end Alembic commands ###
