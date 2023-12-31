"""Database creation

Revision ID: 0604d8d15cd3
Revises: 
Create Date: 2023-07-13 20:48:51.106154

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0604d8d15cd3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_name', sa.String(length=100), nullable=False),
    sa.Column('image_size', sa.String(), nullable=False),
    sa.Column('last_edit_at', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('images')
    # ### end Alembic commands ###
