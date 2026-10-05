from typing import Annotated

from fastapi import Depends

from exceptions import EntityNotFoundException
from repositories import SerieRepositoryDep
from schemas.serie import GeneroSerie, SerieFiltros, SerieListRead, SerieRead
from models.serie import Serie
from models.conteudo import ApiFonte, TipoConteudo
from .conteudo import ConteudoServiceDep


class SerieService:
    def __init__(
        self, 
        serie_repository: SerieRepositoryDep,
        conteudo_service: ConteudoServiceDep
    ):
        self.serie_repository = serie_repository
        self.conteudo_service = conteudo_service

    def get_serie_from_db(self, serie_id: int) -> Serie | None:
        return self.serie_repository.get_serie_by_id_externo(serie_id)

    def get_serie_from_api_and_update_database(self, serie_id: int) -> tuple[SerieRead, Serie]:
        conteudo = self.conteudo_service.get_or_create_conteudo(
            id_externo=serie_id,
            api_fonte=ApiFonte.TMDB,
            tipo=TipoConteudo.SERIE
        )
        result = self.serie_repository.get_serie_and_update_database(serie_id, conteudo)
        if not result:
            raise EntityNotFoundException("Série", serie_id)

        return result

    def search_series(
        self, busca: str | None, filtros: SerieFiltros, page: int = 1
    ) -> tuple[list[SerieListRead], int, int]:
        return self.serie_repository.search_series(busca=busca, filtros=filtros, page=page)

    def list_generos(self) -> list[GeneroSerie]:
        return self.serie_repository.list_generos()

    def list_series_em_alta(self, page: int = 1) -> tuple[list[SerieListRead], int, int]:
        return self.serie_repository.list_series_em_alta(page=page)

    def list_series_populares(self, page: int = 1) -> tuple[list[SerieListRead], int, int]:
        return self.serie_repository.list_series_populares(page=page)


SerieServiceDep = Annotated[SerieService, Depends(SerieService)]
