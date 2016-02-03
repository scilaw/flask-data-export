"""empty message

Revision ID: e4d25b67533d
Revises: 09b1d39ebba2
Create Date: 2016-02-03 01:04:51.914372

"""

# revision identifiers, used by Alembic.
revision = 'e4d25b67533d'
down_revision = '09b1d39ebba2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('export_job',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('dataset_name', sa.String(length=255), nullable=True),
    sa.Column('do_sampling', sa.Boolean(), nullable=True),
    sa.Column('sample_percent', sa.SmallInteger(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('export_job_include_value',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('job_id', sa.Integer(), nullable=True),
    sa.Column('variable_name', sa.String(length=255), nullable=True),
    sa.Column('variable_value', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['job_id'], ['export_job.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('export_job_select_variable',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('job_id', sa.Integer(), nullable=True),
    sa.Column('selected_variable', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['job_id'], ['export_job.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('export_job_select_variable')
    op.drop_table('export_job_include_value')
    op.drop_table('export_job')
    ### end Alembic commands ###
