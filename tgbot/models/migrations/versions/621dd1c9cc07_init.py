"""init

Revision ID: 621dd1c9cc07
Revises: 89a1568cfc1e
Create Date: 2022-04-17 12:53:28.765192

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '621dd1c9cc07'
down_revision = '89a1568cfc1e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('language', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
