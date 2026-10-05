from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from constants import HEADERS_TMDB, PARAMS_TMDB, TMDB_API_URL
from database import SessionDep
from mappers.filme import FilmeMapper
from models.conteudo import ApiFonte, Conteudo, TipoConteudo
from models.filme import Filme
from repositories.conteudo import ConteudoRepositoryDep
from schemas.filme import FilmeFiltros, FilmeListRead, FilmeRead, GeneroFilme
from utils import get_data, str_to_date


class FilmeRepository:
    def __init__(self, session: SessionDep, conteudo_repository: ConteudoRepositoryDep):
        self.session = session
        self.conteudo_repository = conteudo_repository

    def get_filme_from_api(self, filme_id: int) -> FilmeRead | None:
        data = get_data(
            f"{TMDB_API_URL}/movie/{filme_id}",
            params=PARAMS_TMDB,
            headers=HEADERS_TMDB,
        )

        if data.get("success") is False:
            return None

        return FilmeMapper.map_filme(data)

    def get_filme_by_id_externo(self, id_externo: int) -> Filme | None:
        return self.session.scalar(
            select(Filme)
            .join(Filme.conteudo)
            .where(
                Conteudo.id_externo == id_externo,
                Conteudo.api_fonte == ApiFonte.TMDB,
                Conteudo.tipo == TipoConteudo.FILME,
            )
        )

    def get_filme_by_conteudo_id(self, conteudo_id: int) -> Filme | None:
        return self.session.scalar(
            select(Filme).where(Filme.conteudo_id == conteudo_id)
        )

    def create_filme(self, filme: Filme) -> Filme:
        self.session.add(filme)
        self.session.flush()
        return filme

    def update_filme(self, filme: Filme) -> Filme:
        self.session.flush()
        return filme

    def create_or_update_filme(self, filme_from_api: FilmeRead, conteudo: Conteudo) -> Filme:
        filme = self.get_filme_by_conteudo_id(conteudo.id)
        if filme:
            filme.titulo = filme_from_api.titulo
            filme.titulo_original = filme_from_api.titulo_original
            filme.status = filme_from_api.status
            filme.capa = FilmeMapper.unmap_image(filme_from_api.imagens.capa)
            filme.banner = FilmeMapper.unmap_image(filme_from_api.imagens.banner)
            filme.data_lancamento = str_to_date(filme_from_api.data_lancamento)
            return self.update_filme(filme)

        filme_db = Filme(
            conteudo_id=conteudo.id,
            titulo=filme_from_api.titulo,
            titulo_original=filme_from_api.titulo_original,
            status=filme_from_api.status,
            capa=FilmeMapper.unmap_image(filme_from_api.imagens.capa),
            banner=FilmeMapper.unmap_image(filme_from_api.imagens.banner),
            data_lancamento=str_to_date(filme_from_api.data_lancamento),
        )
        return self.create_filme(filme_db)

    def get_filme_and_update_database(
        self, filme_id: int, conteudo: Conteudo
    ) -> tuple[FilmeRead, Filme] | None:
        filme_api = self.get_filme_from_api(filme_id)
        if not filme_api:
            return None

        filme_db = self.create_or_update_filme(filme_api, conteudo)

        return filme_api, filme_db

    def search_filmes(
        self, busca: str | None, filtros: FilmeFiltros, page: int = 1
    ) -> tuple[list[FilmeListRead], int, int]:
        params = PARAMS_TMDB.copy()
        params["page"] = page

        if busca:
            # /search/movie não aceita os filtros do /discover
            params["query"] = busca
            url = f"{TMDB_API_URL}/search/movie"
        else:
            # Sem busca, lista por /discover aplicando os filtros
            url = f"{TMDB_API_URL}/discover/movie"
            if filtros.generos:
                params["with_genres"] = ",".join(str(genero_id) for genero_id in filtros.generos)
            if filtros.ano is not None:
                params["primary_release_year"] = filtros.ano
            if filtros.nota_minima is not None:
                params["vote_average.gte"] = filtros.nota_minima
            params["sort_by"] = f"{filtros.ordenar_por.value}.{filtros.ordem.value}"

        data = get_data(
            url,
            params=params,
            headers=HEADERS_TMDB,
        )

        filmes = FilmeMapper.map_filmes(data.get("results", []))
        total_pages = data.get("total_pages", 0)
        total_results = data.get("total_results", 0)

        return filmes, total_pages, total_results

    def list_generos(self) -> list[GeneroFilme]:
        data = get_data(
            f"{TMDB_API_URL}/genre/movie/list",
            params=PARAMS_TMDB,
            headers=HEADERS_TMDB,
        )

        return [
            GeneroFilme(id=int(genero["id"]), nome=genero["name"])
            for genero in data.get("genres", [])
        ]

    def list_filmes_em_alta(
        self, page: int = 1
    ) -> tuple[list[FilmeListRead], int, int]:
        params = PARAMS_TMDB.copy()
        params["page"] = page

        data = get_data(
            f"{TMDB_API_URL}/trending/movie/week",
            params=params,
            headers=HEADERS_TMDB,
        )

        filmes = FilmeMapper.map_filmes(data.get("results", []))
        total_pages = data.get("total_pages", 0)
        total_results = data.get("total_results", 0)

        return filmes, total_pages, total_results

    def list_filmes_populares(
        self, page: int = 1
    ) -> tuple[list[FilmeListRead], int, int]:
        params = PARAMS_TMDB.copy()
        params["page"] = page

        data = get_data(
            f"{TMDB_API_URL}/movie/popular",
            params=params,
            headers=HEADERS_TMDB,
        )

        filmes = FilmeMapper.map_filmes(data.get("results", []))
        total_pages = data.get("total_pages", 0)
        total_results = data.get("total_results", 0)

        return filmes, total_pages, total_results

    def list_filmes_em_breve(
        self, page: int = 1
    ) -> tuple[list[FilmeListRead], int, int]:
        params = PARAMS_TMDB.copy()
        params["page"] = page

        data = get_data(
            f"{TMDB_API_URL}/movie/upcoming",
            params=params,
            headers=HEADERS_TMDB,
        )

        filmes = FilmeMapper.map_filmes(data.get("results", []))
        total_pages = data.get("total_pages", 0)
        total_results = data.get("total_results", 0)

        return filmes, total_pages, total_results


FilmeRepositoryDep = Annotated[FilmeRepository, Depends(FilmeRepository)]
