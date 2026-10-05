from datetime import datetime
from enum import Enum

from models.conteudo import TipoConteudo, ApiFonte
from .base import Base


class Ordem(str, Enum):
    ASC = "asc"
    DESC = "desc"


class ImagensConteudo(Base):
    capa: str | None
    banner: str | None

class ConteudoCreate(Base):
    id_externo: int
    api_fonte: ApiFonte
    tipo: TipoConteudo

class ConteudoRead(Base):
    id: int
    id_externo: int
    api_fonte: str
    tipo: TipoConteudo
    data_adicao: datetime
