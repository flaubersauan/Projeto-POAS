from pydantic import Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

from .base import Base


class AvaliacaoCreate(Base):
    conteudo_id: Optional[int] = None
    usuario_id: Optional[int] = None
    estrelas: Decimal = Field(
        ge=1, le=5, multiple_of=0.5, decimal_places=1
    )  # >= 1 e <= 5, step de 0.5
    comentario: Optional[str] = None


class AvaliacaoRead(Base):
    id: int
    conteudo_id: int
    usuario_id: int
    estrelas: Decimal
    comentario: Optional[str]
    data_criacao: datetime
    data_atualizacao: Optional[datetime]


class AvaliacaoUpdate(Base):
    estrelas: Optional[Decimal] = Field(
        default=None, ge=1, le=5, multiple_of=0.5, decimal_places=1
    )  # >= 1 e <= 5, step de 0.5
    comentario: Optional[str] = None
