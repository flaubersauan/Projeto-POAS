from pydantic import Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

from .base import Base


class AvaliacaoCreate(Base):
    estrelas: Decimal = Field(
        ge=1, le=5, multiple_of=0.5, decimal_places=1
    )  # >= 1 e <= 5, step de 0.5
    comentario: Optional[str] = None


class AvaliacaoReadBase(Base):
    id: int
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


class AvaliacaoSerieRead(AvaliacaoReadBase):
    serie_id: int

class AvaliacaoFilmeRead(AvaliacaoReadBase):
    filme_id: int

class AvaliacaoAnimeRead(AvaliacaoReadBase):
    anime_id: int