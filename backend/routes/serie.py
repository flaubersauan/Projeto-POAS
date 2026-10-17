from fastapi import APIRouter, Depends, status

from services import AvaliacaoServiceDep, SerieServiceDep, AssistidoServiceDep
from services.favorito import FavoritoServiceDep
from auth.dependencies import CurrentUsuarioDep
from schemas.pagination.tmdb import TmdbPage, TmdbPagination, TmdbPaginationParams
from schemas.serie import GeneroSerie, SerieFiltros, SerieListRead, SerieRead
from schemas.favorito import SerieFavoritaRead
from schemas.assistido import SerieAssistidaRead
from schemas.pagination.cursor import CursorMediaPaginationParams, CursorPage
from schemas.avaliacao import (
    AvaliacaoConteudoRead,
    AvaliacaoCreate,
    AvaliacaoBase,
    AvaliacaoUpdate,
)

series_router = APIRouter(prefix="/series", tags=["Séries"])


@series_router.get("", response_model=TmdbPage[SerieListRead])
def buscar_series(
    serie_service: SerieServiceDep,
    filtros: SerieFiltros = Depends(SerieFiltros.as_dependency),
    busca: str | None = None,
    paginacao: TmdbPaginationParams = Depends(),
):
    series, total_pages, total_results = serie_service.search_series(
        busca=busca, filtros=filtros, page=paginacao.page
    )

    return TmdbPage(
        data=series,
        pagination=TmdbPagination(
            page=paginacao.page,
            total_pages=total_pages,
            total_results=total_results,
            has_more=paginacao.page < total_pages,
        ),
    )


@series_router.get("/em-alta", response_model=TmdbPage[SerieListRead])
def listar_series_em_alta(
    serie_service: SerieServiceDep,
    paginacao: TmdbPaginationParams = Depends(),
):
    series, total_pages, total_results = serie_service.list_series_em_alta(
        page=paginacao.page
    )

    return TmdbPage(
        data=series,
        pagination=TmdbPagination(
            page=paginacao.page,
            total_pages=total_pages,
            total_results=total_results,
            has_more=paginacao.page < total_pages,
        ),
    )


@series_router.get("/populares", response_model=TmdbPage[SerieListRead])
def listar_series_populares(
    serie_service: SerieServiceDep,
    paginacao: TmdbPaginationParams = Depends(),
):
    series, total_pages, total_results = serie_service.list_series_populares(
        page=paginacao.page
    )

    return TmdbPage(
        data=series,
        pagination=TmdbPagination(
            page=paginacao.page,
            total_pages=total_pages,
            total_results=total_results,
            has_more=paginacao.page < total_pages,
        ),
    )


@series_router.get("/generos", response_model=list[GeneroSerie])
def listar_generos_series(serie_service: SerieServiceDep):
    return serie_service.list_generos()


@series_router.get("/favoritas", response_model=CursorPage[SerieFavoritaRead])
def listar_series_favoritas(
    current_user: CurrentUsuarioDep,
    favorito_service: FavoritoServiceDep,
    paging_params: CursorMediaPaginationParams = Depends(),
):
    series, paging = favorito_service.list_favoritos_serie(
        current_user.id,
        paging_params.cursor,
        paging_params.limit,
        paging_params.ordenacao,
    )
    return CursorPage(data=series, pagination=paging)


@series_router.get("/assistidas", response_model=CursorPage[SerieAssistidaRead])
def listar_series_assistidas(
    current_user: CurrentUsuarioDep,
    assistido_service: AssistidoServiceDep,
    paging_params: CursorMediaPaginationParams = Depends(),
):
    series, paging = assistido_service.list_assistidos_serie(
        current_user.id,
        paging_params.cursor,
        paging_params.limit,
        paging_params.ordenacao,
    )
    return CursorPage(data=series, pagination=paging)


@series_router.get("/{serie_id}", response_model=SerieRead)
def buscar_serie(serie_id: int, serie_service: SerieServiceDep):
    serie, _ = serie_service.get_serie_from_api_and_update_database(serie_id=serie_id)
    return serie


@series_router.get(
    "/{serie_id}/avaliacoes", response_model=CursorPage[AvaliacaoConteudoRead]
)
def listar_avaliacoes_da_serie(
    serie_id: int,
    avaliacao_service: AvaliacaoServiceDep,
    paging_params: CursorMediaPaginationParams = Depends(),
):
    avaliacoes, paging = avaliacao_service.list_avaliacoes_serie(
        serie_id,
        paging_params.cursor,
        paging_params.limit,
        paging_params.ordenacao,
    )
    return CursorPage(data=avaliacoes, pagination=paging)


@series_router.post(
    "/{serie_id}/avaliacoes",
    response_model=AvaliacaoBase,
    status_code=status.HTTP_201_CREATED,
)
def criar_avaliacao_da_serie(
    serie_id: int,
    avaliacao: AvaliacaoCreate,
    current_user: CurrentUsuarioDep,
    avaliacao_service: AvaliacaoServiceDep,
):
    return avaliacao_service.create_avaliacao(
        avaliacao, serie_id, current_user.id, tipo_conteudo="serie"
    )


@series_router.patch("/{serie_id}/avaliacoes", response_model=AvaliacaoBase)
def atualizar_avaliacao_da_serie(
    serie_id: int,
    avaliacao: AvaliacaoUpdate,
    current_user: CurrentUsuarioDep,
    avaliacao_service: AvaliacaoServiceDep,
):
    return avaliacao_service.update_avaliacao(
        avaliacao, serie_id, current_user.id, tipo_conteudo="serie"
    )


@series_router.delete("/{serie_id}/avaliacoes", status_code=status.HTTP_204_NO_CONTENT)
def remover_avaliacao_da_serie(
    serie_id: int,
    current_user: CurrentUsuarioDep,
    avaliacao_service: AvaliacaoServiceDep,
):
    avaliacao_service.delete_avaliacao(serie_id, current_user.id, "serie")


@series_router.post("/{serie_id}/favoritos", status_code=status.HTTP_204_NO_CONTENT)
def adicionar_serie_aos_favoritos(
    serie_id: int, current_user: CurrentUsuarioDep, favorito_service: FavoritoServiceDep
):
    favorito_service.add_favorito_serie(serie_id, current_user.id)


@series_router.post("/{serie_id}/assistidos", status_code=status.HTTP_204_NO_CONTENT)
def adicionar_serie_aos_assistidos(
    serie_id: int,
    current_user: CurrentUsuarioDep,
    assistido_service: AssistidoServiceDep,
):
    assistido_service.add_assistido_serie(serie_id, current_user.id)


@series_router.delete("/{serie_id}/favoritos", status_code=status.HTTP_204_NO_CONTENT)
def remover_serie_dos_favoritos(
    serie_id: int, current_user: CurrentUsuarioDep, favorito_service: FavoritoServiceDep
):
    favorito_service.remove_favorito_serie(serie_id, current_user.id)


@series_router.delete("/{serie_id}/assistidos", status_code=status.HTTP_204_NO_CONTENT)
def remover_serie_dos_assistidos(
    serie_id: int,
    current_user: CurrentUsuarioDep,
    assistido_service: AssistidoServiceDep,
):
    assistido_service.remove_assistido_serie(serie_id, current_user.id)
