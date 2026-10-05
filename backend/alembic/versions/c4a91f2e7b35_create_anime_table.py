"""create_anime_table

Revision ID: c4a91f2e7b35
Revises: 1d7ce2e5b3be
Create Date: 2026-10-03 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4a91f2e7b35'
down_revision: Union[str, Sequence[str], None] = '1d7ce2e5b3be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('anime',
    sa.Column('conteudo_id', sa.BigInteger(), nullable=False),
    sa.Column('titulo', sa.String(length=255), nullable=False),
    sa.Column('titulo_original', sa.String(length=255), nullable=False),
    sa.Column('status', sa.String(length=255), nullable=False),
    sa.Column('capa', sa.String(length=512), nullable=True),
    sa.Column('banner', sa.String(length=512), nullable=True),
    sa.Column('data_lancamento', sa.Date(), nullable=True),
    sa.Column('data_atualizacao', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['conteudo_id'], ['conteudo.id'], ),
    sa.PrimaryKeyConstraint('conteudo_id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('anime')
