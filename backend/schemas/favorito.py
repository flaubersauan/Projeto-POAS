from datetime import datetime, date

from .base import Base
from .conteudo import ImagensConteudo


class FavoritoCreate(Base):
    conteudo_id: int
    usuario_id: int

class FilmeFavoritoRead(Base):
    id: int
    titulo: str
    titulo_original: str
    status: str
    imagens: ImagensConteudo
    data_lancamento: date | None = None
    data_adicao: datetime

class SerieFavoritaRead(Base):
    id: int
    titulo: str
    titulo_original: str
    status: str
    imagens: ImagensConteudo
    data_lancamento: date | None = None
    data_adicao: datetime

class AnimeFavoritoRead(Base):
    id: int
    titulo: str
    titulo_original: str
    status: str
    imagens: ImagensConteudo
    data_lancamento: date | None = None
    data_adicao: datetime

# class FavoritoRead(Base):
#     id: int
#     conteudo_id: int
#     usuario_id: int
#     data_adicao: datetime


# class FavoritoUpdate(BaseModel):
# pass
