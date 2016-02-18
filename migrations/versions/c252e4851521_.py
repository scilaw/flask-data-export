"""empty message

Revision ID: c252e4851521
Revises: 5f026d9a6649
Create Date: 2016-02-04 22:49:52.089265

"""

# revision identifiers, used by Alembic.
revision = 'c252e4851521'
down_revision = '5f026d9a6649'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('downloads',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('job_id', sa.Integer(), nullable=True),
    sa.Column('ip', sa.String(length=45), nullable=True),
    sa.Column('downloaded_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['job_id'], ['export_job.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('downloads')
    ### end Alembic commands ###