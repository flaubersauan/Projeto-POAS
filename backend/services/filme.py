from typing import Annotated

from fastapi import Depends

from exceptions import EntityNotFoundException
from models.conteudo import ApiFonte, TipoConteudo
from models.filme import Filme
from repositories import FilmeRepositoryDep
from schemas.filme import FilmeFiltros, FilmeListRead, FilmeRead, GeneroFilme
from .conteudo import ConteudoServiceDep


class FilmeService:
    def __init__(
        self,
        filme_repository: FilmeRepositoryDep,
        conteudo_service: ConteudoServiceDep,
    ):
        self.filme_repository = filme_repository
        self.conteudo_service = conteudo_service

    def get_filme_from_db(self, filme_id: int) -> Filme | None:
        return self.filme_repository.get_filme_by_id_externo(filme_id)

    def get_filme_from_api_and_update_database(self, filme_id: int) -> tuple[FilmeRead, Filme]:
        conteudo = self.conteudo_service.get_or_create_conteudo(
            id_externo=filme_id,
            api_fonte=ApiFonte.TMDB,
            tipo=TipoConteudo.FILME,
        )
        result = self.filme_repository.get_filme_and_update_database(filme_id, conteudo)
        if not result:
            raise EntityNotFoundException("Filme", filme_id)

        return result

    def get_filme(self, filme_id: int) -> FilmeRead:
        filme, _ = self.get_filme_from_api_and_update_database(filme_id)
        return filme

    def search_filmes(
        self, busca: str | None, filtros: FilmeFiltros, page: int = 1
    ) -> tuple[list[FilmeListRead], int, int]:
        return self.filme_repository.search_filmes(busca=busca, filtros=filtros, page=page)

    def list_generos(self) -> list[GeneroFilme]:
        return self.filme_repository.list_generos()

    def list_filmes_em_alta(
        self, page: int = 1
    ) -> tuple[list[FilmeListRead], int, int]:
        return self.filme_repository.list_filmes_em_alta(page=page)

    def list_filmes_populares(
        self, page: int = 1
    ) -> tuple[list[FilmeListRead], int, int]:
        return self.filme_repository.list_filmes_populares(page=page)

    def list_filmes_em_breve(
        self, page: int = 1
    ) -> tuple[list[FilmeListRead], int, int]:
        return self.filme_repository.list_filmes_em_breve(page=page)


FilmeServiceDep = Annotated[FilmeService, Depends(FilmeService)]
