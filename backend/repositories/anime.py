from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from constants import HEADERS_KITSU, KITSU_API_URL
from database import SessionDep
from exceptions import ExternalAPIException
from mappers.anime import AnimeMapper
from models.anime import Anime
from models.conteudo import ApiFonte, Conteudo, TipoConteudo
from schemas.anime import AnimeFiltros, AnimeRead, CategoriaRead
from schemas.conteudo import Ordem
from utils import get_data, str_to_date


class AnimeRepository:
    """Acesso à API do Kitsu e à tabela `anime` do banco de dados."""

    def __init__(self, session: SessionDep):
        self.session = session

    # ── API Kitsu ─────────────────────────────────────────────────────────

    def _fetch_animes(self, params: dict) -> tuple[list[AnimeRead], int]:
        params.setdefault("include", "genres,categories")
        params.setdefault("fields[genres]", "name")
        params.setdefault("fields[categories]", "title")

        data = get_data(f"{KITSU_API_URL}/anime", params=params, headers=HEADERS_KITSU)

        animes = AnimeMapper.map_animes(data.get("data", []), data.get("included", []))
        total_results = data.get("meta", {}).get("count", 0)

        return animes, total_results

    def _build_filter_params(self, filtros: AnimeFiltros, limit: int, offset: int) -> dict:
        params: dict = {"page[limit]": limit, "page[offset]": offset}

        if filtros.busca:
            params["filter[text]"] = filtros.busca
        if filtros.categorias:
            params["filter[categories]"] = ",".join(filtros.categorias)
        if filtros.formato:
            params["filter[subtype]"] = filtros.formato.value
        if filtros.status:
            status_kitsu = AnimeMapper.STATUS_TO_KITSU.get(filtros.status)
            if status_kitsu:
                params["filter[status]"] = status_kitsu
        if filtros.classificacao_etaria:
            params["filter[ageRating]"] = filtros.classificacao_etaria.value
        if filtros.ano is not None:
            params["filter[year]"] = str(filtros.ano)
        elif filtros.ano_inicio is not None and filtros.ano_fim is not None:
            params["filter[year]"] = f"{filtros.ano_inicio}..{filtros.ano_fim}"
        if filtros.temporada:
            params["filter[season]"] = filtros.temporada.value
            if filtros.ano is not None:
                params["filter[seasonYear]"] = str(filtros.ano)
        if filtros.nota_minima is not None:
            params["filter[averageRating]"] = f"{filtros.nota_minima:g}..100"

        # Com busca textual e sem ordenação explícita, deixa o Kitsu ordenar por relevância.
        # Sem busca, lista por popularidade.
        if not filtros.busca or filtros.ordenacao_explicita:
            sort = filtros.ordenar_por.value
            if filtros.ordem == Ordem.DESC:
                sort = f"-{sort}"
            params["sort"] = sort

        return params

    def search_animes(
        self, filtros: AnimeFiltros, limit: int, offset: int
    ) -> tuple[list[AnimeRead], int]:
        params = self._build_filter_params(filtros, limit, offset)
        return self._fetch_animes(params)

    def list_animes_em_alta(
        self, limit: int, offset: int
    ) -> tuple[list[AnimeRead], int]:
        # /trending/anime do Kitsu não retorna meta.count,
        # então usa o /anime ordenado por popularidade para manter a paginação
        params = {
            "page[limit]": limit,
            "page[offset]": offset,
            "sort": "popularityRank",
        }
        return self._fetch_animes(params)

    def list_animes_populares(
        self, limit: int, offset: int
    ) -> tuple[list[AnimeRead], int]:
        params = {
            "page[limit]": limit,
            "page[offset]": offset,
            "sort": "-userCount",
        }
        return self._fetch_animes(params)

    def list_animes_em_breve(
        self, limit: int, offset: int
    ) -> tuple[list[AnimeRead], int]:
        params = {
            "page[limit]": limit,
            "page[offset]": offset,
            "filter[status]": "upcoming",
            "sort": "-startDate",
        }
        return self._fetch_animes(params)

    def list_categorias(
        self, limit: int, offset: int
    ) -> tuple[list[CategoriaRead], int]:
        params = {
            "page[limit]": limit,
            "page[offset]": offset,
            "sort": "-totalMediaCount",
        }

        data = get_data(f"{KITSU_API_URL}/categories", params=params, headers=HEADERS_KITSU)

        categorias = AnimeMapper.map_categorias(data.get("data", []))
        total_results = data.get("meta", {}).get("count", 0)

        return categorias, total_results

    def get_anime_from_api(self, anime_id: int) -> AnimeRead | None:
        params = {
            "include": "genres,categories",
            "fields[genres]": "name",
            "fields[categories]": "title",
        }

        try:
            data = get_data(
                f"{KITSU_API_URL}/anime/{anime_id}",
                params=params,
                headers=HEADERS_KITSU,
            )
        except ExternalAPIException as exc:
            if exc.status_code == 404:
                return None
            raise

        item = data.get("data")
        if not item:
            return None

        return AnimeMapper.map_anime(item, data.get("included", []))

    # ── Banco de dados ────────────────────────────────────────────────────

    def get_anime_by_id_externo(self, id_externo: int) -> Anime | None:
        return self.session.scalar(
            select(Anime)
            .join(Anime.conteudo)
            .where(
                Conteudo.id_externo == id_externo,
                Conteudo.api_fonte == ApiFonte.KITSU,
                Conteudo.tipo == TipoConteudo.ANIME,
            )
        )

    def get_anime_by_conteudo_id(self, conteudo_id: int) -> Anime | None:
        return self.session.scalar(
            select(Anime).where(Anime.conteudo_id == conteudo_id)
        )

    def create_anime(self, anime: Anime) -> Anime:
        self.session.add(anime)
        self.session.flush()
        return anime

    def update_anime(self, anime: Anime) -> Anime:
        self.session.flush()
        return anime

    def create_or_update_anime(self, anime_from_api: AnimeRead, conteudo: Conteudo) -> Anime:
        titulo_original = (
            anime_from_api.titulos.get("ja_jp")
            or anime_from_api.titulos.get("en_jp")
            or anime_from_api.titulo_canonico
        )
        data_lancamento = str_to_date(anime_from_api.data_inicio)

        anime = self.get_anime_by_conteudo_id(conteudo.id)
        if anime:
            anime.titulo = anime_from_api.titulo_canonico
            anime.titulo_original = titulo_original
            anime.status = anime_from_api.status.value
            anime.capa = anime_from_api.imagens.capa
            anime.banner = anime_from_api.imagens.banner
            anime.data_lancamento = data_lancamento
            return self.update_anime(anime)

        anime_db = Anime(
            conteudo_id=conteudo.id,
            titulo=anime_from_api.titulo_canonico,
            titulo_original=titulo_original,
            status=anime_from_api.status.value,
            capa=anime_from_api.imagens.capa,
            banner=anime_from_api.imagens.banner,
            data_lancamento=data_lancamento,
        )
        return self.create_anime(anime_db)

    def get_anime_and_update_database(
        self, anime_id: int, conteudo: Conteudo
    ) -> tuple[AnimeRead, Anime] | None:
        anime_api = self.get_anime_from_api(anime_id)
        if not anime_api:
            return None

        anime_db = self.create_or_update_anime(anime_api, conteudo)

        return anime_api, anime_db


AnimeRepositoryDep = Annotated[AnimeRepository, Depends(AnimeRepository)]
