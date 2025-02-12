"""create telefone table

Revision ID: create_telefone_table
Revises: 
Create Date: 2024-02-12

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'create_telefone_table'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'telefone',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('numero', sa.String(length=20), nullable=False),
        sa.Column('tipo', sa.String(length=20), nullable=False),
        sa.Column('pessoa_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.now),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=datetime.now),
        sa.Column('deleted', sa.Boolean(), nullable=False, default=False),
        sa.ForeignKeyConstraint(['pessoa_id'], ['pessoa.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_telefone_id'), 'telefone', ['id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_telefone_id'), table_name='telefone')
    op.drop_table('telefone')