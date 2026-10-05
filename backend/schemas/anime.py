from enum import Enum
from typing import Annotated

from fastapi import Query
from pydantic import Field

from .base import Base
from .conteudo import Ordem


class ImagensAnime(Base):
    capa: str | None = None #posterImage
    banner: str | None = None #coverImage

class GeneroAnime(Base):
    id: int
    nome: str

class CategoriaAnime(Base):
    id: int
    nome: str

class CategoriaRead(Base):
    """Categoria do Kitsu retornada pela listagem de /animes/categorias."""

    id: int
    nome: str
    slug: str
    descricao: str | None = None
    total_midias: int | None = None

class StatusAnime(str, Enum):
    ANDAMENTO = "Em andamento" #current
    FINALIZADO = "Finalizado" #finished
    A_SER_ANUNCIADO = "A ser anunciado" #tba
    NAO_LANCADO = "Não lançado" #unreleased
    POR_VIR = "Por vir" #upcoming
    DESCONHECIDO = "Desconhecido" #fallback para status não mapeados

class FormatoAnime(str, Enum):
    TV = "TV"
    FILME = "movie"
    OVA = "OVA"
    ONA = "ONA"
    ESPECIAL = "special"
    MUSICA = "music"

class ClassificacaoEtaria(str, Enum):
    LIVRE = "G"
    PG = "PG"
    R = "R"
    R18 = "R18"

class TemporadaAnime(str, Enum):
    INVERNO = "winter"
    PRIMAVERA = "spring"
    VERAO = "summer"
    OUTONO = "fall"

class OrdenacaoAnime(str, Enum):
    POPULARIDADE = "popularityRank"
    NOTA = "ratingRank"
    MEDIA = "averageRating"
    DATA_INICIO = "startDate"
    USUARIOS = "userCount"

class AnimeRead(Base):
    id: int
    titulos: dict[str, str] = Field(default_factory=dict)
    titulo_canonico: str
    descricao: str | None = None
    status: StatusAnime
    data_inicio: str | None = None
    data_fim: str | None = None
    quantidade_episodios: int | None = None
    duracao_episodios: int | None = None
    imagens: ImagensAnime
    generos: list[GeneroAnime] = Field(default_factory=list)
    categorias: list[CategoriaAnime] = Field(default_factory=list)

class AnimeFiltros(Base):
    """Filtros de pesquisa de animes, montados como query params da rota /animes.

    Sem 'busca', a listagem é feita por popularidade.

    A construção a partir dos query params é feita por `as_dependency`, pois
    modelos Pydantic usados diretamente com Depends() não suportam campos
    do tipo lista como query params.
    """

    busca: str | None = None
    categorias: list[str] | None = None # slugs do Kitsu, ex: categorias=action&categorias=drama
    formato: FormatoAnime | None = None
    status: StatusAnime | None = None
    classificacao_etaria: ClassificacaoEtaria | None = None
    ano: int | None = Field(default=None, ge=1900, le=2100)
    ano_inicio: int | None = Field(default=None, ge=1900, le=2100)
    ano_fim: int | None = Field(default=None, ge=1900, le=2100)
    temporada: TemporadaAnime | None = None
    nota_minima: float | None = Field(default=None, ge=0, le=100) # escala 0-100 do Kitsu
    ordenar_por: OrdenacaoAnime = OrdenacaoAnime.POPULARIDADE
    ordem: Ordem = Ordem.ASC # ranks do Kitsu: asc = melhor posição primeiro
    ordenacao_explicita: bool = Field(default=False, exclude=True) # preenchido pelo as_dependency

    @classmethod
    def as_dependency(
        cls,
        busca: str | None = None,
        categorias: Annotated[list[str] | None, Query()] = None,
        formato: FormatoAnime | None = None,
        status: StatusAnime | None = None,
        classificacao_etaria: ClassificacaoEtaria | None = None,
        ano: Annotated[int | None, Query(ge=1900, le=2100)] = None,
        ano_inicio: Annotated[int | None, Query(ge=1900, le=2100)] = None,
        ano_fim: Annotated[int | None, Query(ge=1900, le=2100)] = None,
        temporada: TemporadaAnime | None = None,
        nota_minima: Annotated[float | None, Query(ge=0, le=100)] = None,
        ordenar_por: OrdenacaoAnime | None = None,
        ordem: Ordem | None = None,
    ) -> "AnimeFiltros":
        return cls(
            busca=busca,
            categorias=categorias,
            formato=formato,
            status=status,
            classificacao_etaria=classificacao_etaria,
            ano=ano,
            ano_inicio=ano_inicio,
            ano_fim=ano_fim,
            temporada=temporada,
            nota_minima=nota_minima,
            ordenar_por=ordenar_por or OrdenacaoAnime.POPULARIDADE,
            ordem=ordem or Ordem.ASC,
            ordenacao_explicita=ordenar_por is not None or ordem is not None,
        )
