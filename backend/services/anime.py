from typing import Annotated

from fastapi import Depends, HTTPException, status

from exceptions import EntityNotFoundException
from models.anime import Anime
from models.conteudo import ApiFonte, TipoConteudo
from repositories import AnimeRepositoryDep
from schemas.anime import AnimeFiltros, AnimeRead, CategoriaRead
from .conteudo import ConteudoServiceDep


class AnimeService:
    def __init__(
        self,
        anime_repository: AnimeRepositoryDep,
        conteudo_service: ConteudoServiceDep,
    ):
        self.anime_repository = anime_repository
        self.conteudo_service = conteudo_service

    def _validar_filtros(self, filtros: AnimeFiltros):
        if filtros.ano is not None and (
            filtros.ano_inicio is not None or filtros.ano_fim is not None
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Use 'ano' ou o intervalo 'ano_inicio'/'ano_fim', não ambos.",
            )

        if (filtros.ano_inicio is None) != (filtros.ano_fim is None):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="'ano_inicio' e 'ano_fim' devem ser informados juntos.",
            )

        if (
            filtros.ano_inicio is not None
            and filtros.ano_fim is not None
            and filtros.ano_inicio > filtros.ano_fim
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="'ano_inicio' não pode ser maior que 'ano_fim'.",
            )

        if filtros.temporada is not None and filtros.ano is None and (
            filtros.ano_inicio is not None or filtros.ano_fim is not None
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="'temporada' não pode ser combinada com intervalo de anos. "
                "Use 'ano' para definir o ano da temporada.",
            )

    def list_animes(
        self, filtros: AnimeFiltros, limit: int, offset: int
    ) -> tuple[list[AnimeRead], int]:
        self._validar_filtros(filtros)
        return self.anime_repository.search_animes(
            filtros=filtros, limit=limit, offset=offset
        )

    def list_animes_em_alta(
        self, limit: int, offset: int
    ) -> tuple[list[AnimeRead], int]:
        return self.anime_repository.list_animes_em_alta(limit=limit, offset=offset)

    def list_animes_populares(
        self, limit: int, offset: int
    ) -> tuple[list[AnimeRead], int]:
        return self.anime_repository.list_animes_populares(limit=limit, offset=offset)

    def list_animes_em_breve(
        self, limit: int, offset: int
    ) -> tuple[list[AnimeRead], int]:
        return self.anime_repository.list_animes_em_breve(limit=limit, offset=offset)

    def list_categorias(
        self, limit: int, offset: int
    ) -> tuple[list[CategoriaRead], int]:
        return self.anime_repository.list_categorias(limit=limit, offset=offset)

    def get_anime_from_db(self, anime_id: int) -> Anime | None:
        return self.anime_repository.get_anime_by_id_externo(anime_id)

    def get_anime_from_api_and_update_database(self, anime_id: int) -> tuple[AnimeRead, Anime]:
        conteudo = self.conteudo_service.get_or_create_conteudo(
            id_externo=anime_id,
            api_fonte=ApiFonte.KITSU,
            tipo=TipoConteudo.ANIME,
        )
        result = self.anime_repository.get_anime_and_update_database(anime_id, conteudo)
        if not result:
            raise EntityNotFoundException("Anime", anime_id)

        return result

    def get_anime(self, anime_id: int) -> AnimeRead:
        anime, _ = self.get_anime_from_api_and_update_database(anime_id)
        return anime


AnimeServiceDep = Annotated[AnimeService, Depends(AnimeService)]
