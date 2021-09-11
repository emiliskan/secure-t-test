"""Changed delete strategy for comment

Revision ID: 6d82899dc9b6
Revises: 41a65761dc0f
Create Date: 2021-09-12 01:56:33.739927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d82899dc9b6'
down_revision = '41a65761dc0f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('comments_comment_fkey', 'comments', type_='foreignkey')
    op.create_foreign_key(None, 'comments', 'comments', ['comment'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.create_foreign_key('comments_comment_fkey', 'comments', 'comments', ['comment'], ['id'])
    # ### end Alembic commands ###
