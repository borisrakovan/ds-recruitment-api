"""edet application constraints

Revision ID: 4d8b974d7d4a
Revises: 
Create Date: 2022-01-10 16:52:53.569730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d8b974d7d4a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('candidate',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=40), nullable=False),
    sa.Column('surname', sa.String(length=40), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('phone_number', sa.String(length=20), nullable=True),
    sa.Column('expected_salary', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_candidate_created_at'), 'candidate', ['created_at'], unique=False)
    op.create_table('job_advertisement',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=60), nullable=False),
    sa.Column('salary_min', sa.Integer(), nullable=False),
    sa.Column('salary_max', sa.Integer(), nullable=False),
    sa.Column('full_text', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_job_advertisement_created_at'), 'job_advertisement', ['created_at'], unique=False)
    op.create_table('skill',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_skill_created_at'), 'skill', ['created_at'], unique=False)
    op.create_table('candidate_skills',
    sa.Column('candidate_id', sa.Integer(), nullable=False),
    sa.Column('skill_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['candidate_id'], ['candidate.id'], ),
    sa.ForeignKeyConstraint(['skill_id'], ['skill.id'], ),
    sa.PrimaryKeyConstraint('candidate_id', 'skill_id')
    )
    op.create_table('job_application',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('candidate_id', sa.Integer(), nullable=False),
    sa.Column('advertisement_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['advertisement_id'], ['job_advertisement.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['candidate_id'], ['candidate.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_job_application_created_at'), 'job_application', ['created_at'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_job_application_created_at'), table_name='job_application')
    op.drop_table('job_application')
    op.drop_table('candidate_skills')
    op.drop_index(op.f('ix_skill_created_at'), table_name='skill')
    op.drop_table('skill')
    op.drop_index(op.f('ix_job_advertisement_created_at'), table_name='job_advertisement')
    op.drop_table('job_advertisement')
    op.drop_index(op.f('ix_candidate_created_at'), table_name='candidate')
    op.drop_table('candidate')
    # ### end Alembic commands ###