"""empty message

Revision ID: 3e45ffb8236d
Revises: 9ec2cd7f9f5d
Create Date: 2021-05-07 10:34:44.523301

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3e45ffb8236d'
down_revision = '9ec2cd7f9f5d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('author_id', sa.Integer(), nullable=True))
    op.drop_constraint('posts_ibfk_1', 'posts', type_='foreignkey')
    op.create_foreign_key(None, 'posts', 'users', ['author_id'], ['id'])
    op.drop_column('posts', 'author')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('author', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.create_foreign_key('posts_ibfk_1', 'posts', 'users', ['author'], ['id'])
    op.drop_column('posts', 'author_id')
    # ### end Alembic commands ###