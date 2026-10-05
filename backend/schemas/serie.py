from datetime import date
from enum import Enum
from typing import Annotated

from fastapi import Query
from pydantic import Field

from schemas.conteudo import ImagensConteudo, Ordem

from .base import Base

class GeneroSerie(Base):
    id: int
    nome: str

class OrdenacaoSerie(str, Enum):
    POPULARIDADE = "popularity"
    NOTA = "vote_average"
    DATA_LANCAMENTO = "first_air_date"
    TITULO = "name"

class SerieFiltros(Base):
    """Filtros de listagem de séries (usados no /discover/tv do TMDB).

    Ignorados quando 'busca' é informada, pois o /search/tv não aceita filtros.

    A construção a partir dos query params é feita por `as_dependency`, pois
    modelos Pydantic usados diretamente com Depends() não suportam campos
    do tipo lista como query params.
    """

    generos: list[int] | None = None # ids do TMDB, ex: generos=18&generos=35
    ano: int | None = Field(default=None, ge=1900, le=2100)
    nota_minima: float | None = Field(default=None, ge=0, le=10) # escala 0-10 do TMDB
    ordenar_por: OrdenacaoSerie = OrdenacaoSerie.POPULARIDADE
    ordem: Ordem = Ordem.DESC

    @classmethod
    def as_dependency(
        cls,
        generos: Annotated[list[int] | None, Query()] = None,
        ano: Annotated[int | None, Query(ge=1900, le=2100)] = None,
        nota_minima: Annotated[float | None, Query(ge=0, le=10)] = None,
        ordenar_por: OrdenacaoSerie = OrdenacaoSerie.POPULARIDADE,
        ordem: Ordem = Ordem.DESC,
    ) -> "SerieFiltros":
        return cls(
            generos=generos,
            ano=ano,
            nota_minima=nota_minima,
            ordenar_por=ordenar_por,
            ordem=ordem,
        )


class TemporadaSerie(Base):
    id: int
    nome: str
    numero_temporada: int = 0
    quantidade_episodios: int = 0
    descricao: str | None = None
    data_lancamento: date | None = None
    capa: str | None = None

class SerieListRead(Base):
    id: int
    titulo: str
    titulo_original: str
    idioma_original: str
    descricao: str | None = None
    # status: str # TMDB não disponibiliza explicitamente a lista com todos os valores possíveis para Status
    data_lancamento: date | None = None
    imagens: ImagensConteudo
    generos_ids: list[int] = Field(default_factory=list)

class SerieRead(Base):
    id: int
    titulo: str
    titulo_original: str
    idioma_original: str
    descricao: str | None = None
    status: str # TMDB não disponibiliza explicitamente a lista com todos os valores possíveis para Status
    data_lancamento: date | None = None
    imagens: ImagensConteudo
    generos: list[GeneroSerie] = Field(default_factory=list)
    duracao_episodios: list[int]= Field(default_factory=list)
    quantidade_episodios: int = 0
    quantidade_temporadas: int = 0
    temporadas: list[TemporadaSerie] = Field(default_factory=list)