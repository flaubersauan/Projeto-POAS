from datetime import date
from enum import Enum
from typing import Annotated

from fastapi import Query
from pydantic import Field

from .base import Base
from .conteudo import ImagensConteudo, Ordem

class GeneroFilme(Base):
    id: int
    nome: str

class OrdenacaoFilme(str, Enum):
    POPULARIDADE = "popularity"
    NOTA = "vote_average"
    DATA_LANCAMENTO = "primary_release_date"
    TITULO = "title"
    RECEITA = "revenue"

class FilmeFiltros(Base):
    """Filtros de listagem de filmes (usados no /discover/movie do TMDB).

    Ignorados quando 'busca' é informada, pois o /search/movie não aceita filtros.

    A construção a partir dos query params é feita por `as_dependency`, pois
    modelos Pydantic usados diretamente com Depends() não suportam campos
    do tipo lista como query params.
    """

    generos: list[int] | None = None # ids do TMDB, ex: generos=28&generos=12
    ano: int | None = Field(default=None, ge=1900, le=2100)
    nota_minima: float | None = Field(default=None, ge=0, le=10) # escala 0-10 do TMDB
    ordenar_por: OrdenacaoFilme = OrdenacaoFilme.POPULARIDADE
    ordem: Ordem = Ordem.DESC

    @classmethod
    def as_dependency(
        cls,
        generos: Annotated[list[int] | None, Query()] = None,
        ano: Annotated[int | None, Query(ge=1900, le=2100)] = None,
        nota_minima: Annotated[float | None, Query(ge=0, le=10)] = None,
        ordenar_por: OrdenacaoFilme = OrdenacaoFilme.POPULARIDADE,
        ordem: Ordem = Ordem.DESC,
    ) -> "FilmeFiltros":
        return cls(
            generos=generos,
            ano=ano,
            nota_minima=nota_minima,
            ordenar_por=ordenar_por,
            ordem=ordem,
        )

# class ImagensFilme(Base):
#     capa: str | None = None #storage+poster_path
#     banner: str | None = None #storage+backdrop_path

class FilmeListRead(Base):
    id: int
    titulo: str
    titulo_original: str
    idioma_original: str
    descricao: str | None = None
    # status: str # TMDB não disponibiliza explicitamente a lista com todos os valores possíveis para Status
    data_lancamento: date | None = None
    imagens: ImagensConteudo
    generos_ids: list[int] = Field(default_factory=list)

class FilmeRead(Base):
    id: int
    titulo: str
    titulo_original: str
    idioma_original: str
    descricao: str | None = None
    status: str # TMDB não disponibiliza explicitamente a lista com todos os valores possíveis para Status
    data_lancamento: date | None = None
    duracao_minutos: int = 0 # 0 é o padrão da api do TMDB
    imagens: ImagensConteudo
    generos: list[GeneroFilme] = Field(default_factory=list)