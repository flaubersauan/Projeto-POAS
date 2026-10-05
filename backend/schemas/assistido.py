from datetime import date, datetime

from .base import Base
from .conteudo import ImagensConteudo


class FilmeAssistidoRead(Base):
    id: int
    titulo: str
    titulo_original: str
    status: str
    imagens: ImagensConteudo
    data_lancamento: date | None = None
    data_adicao: datetime


class SerieAssistidaRead(Base):
    id: int
    titulo: str
    titulo_original: str
    status: str
    imagens: ImagensConteudo
    data_lancamento: date | None = None
    data_adicao: datetime


class AnimeAssistidoRead(Base):
    id: int
    titulo: str
    titulo_original: str
    status: str
    imagens: ImagensConteudo
    data_lancamento: date | None = None
    data_adicao: datetime
