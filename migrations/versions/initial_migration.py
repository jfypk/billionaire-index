"""Initial migration

Revision ID: initial_migration
Revises: 
Create Date: 2024-03-01

"""
from alembic import op
import sqlalchemy as sa

revision = 'initial_migration'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'billionaires',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('net_worth', sa.Float(), nullable=False),
        sa.Column('social_score', sa.Float(), nullable=False),
        sa.Column('environmental_score', sa.Float(), nullable=False),
        sa.Column('political_score', sa.Float(), nullable=False),
        sa.Column('philanthropy_score', sa.Float(), nullable=False),
        sa.Column('cultural_score', sa.Float(), nullable=False),
        sa.Column('overall_score', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'votes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('weight', sa.Float(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'reports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('billionaire_id', sa.String(), nullable=False),
        sa.Column('evidence', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['billionaire_id'], ['billionaires.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('reports')
    op.drop_table('votes')
    op.drop_table('billionaires')
