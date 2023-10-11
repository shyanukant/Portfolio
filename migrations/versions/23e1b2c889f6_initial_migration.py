"""initial migration

Revision ID: 23e1b2c889f6
Revises: 
Create Date: 2023-10-10 11:21:31.275826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23e1b2c889f6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contact',
    sa.Column('Sno', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('phone', sa.String(length=12), nullable=False),
    sa.Column('message', sa.String(length=300), nullable=True),
    sa.Column('file', sa.String(length=500), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('Sno')
    )
    op.create_table('project_post',
    sa.Column('Sno', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('slug', sa.String(length=30), nullable=False),
    sa.Column('img_file', sa.String(length=500), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('project_link', sa.String(length=50), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('Sno'),
    sa.UniqueConstraint('slug')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('project_post')
    op.drop_table('contact')
    # ### end Alembic commands ###