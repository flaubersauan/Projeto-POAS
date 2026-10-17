from fastapi import APIRouter, Depends, status

from auth.dependencies import CurrentUsuarioDep
from schemas.anime import AnimeFiltros, AnimeRead, CategoriaRead
from schemas.assistido import AnimeAssistidoRead
from schemas.pagination.cursor import CursorMediaPaginationParams, CursorPage
from schemas.favorito import AnimeFavoritoRead
from schemas.pagination.kitsu import (
    KitsuPaginationParams,
    KitsuPage,
    KitsuPagination,
)
from services import (
    AnimeServiceDep,
    AssistidoServiceDep,
    FavoritoServiceDep,
    AvaliacaoServiceDep,
)
from schemas.avaliacao import (
    AvaliacaoCreate,
    AvaliacaoBase,
    AvaliacaoConteudoRead,
    AvaliacaoUpdate,
)

animes_router = APIRouter(prefix="/animes", tags=["animes"])


@animes_router.get("", response_model=KitsuPage[AnimeRead])
def buscar_animes(
    anime_service: AnimeServiceDep,
    filtros: AnimeFiltros = Depends(AnimeFiltros.as_dependency),
    paginacao: KitsuPaginationParams = Depends(),
):
    animes, total_results = anime_service.list_animes(
        filtros=filtros, paginacao=paginacao
    )

    return KitsuPage(
        data=animes,
        pagination=KitsuPagination(
            page=paginacao.page,
            total_results=total_results,
            has_more=paginacao.page * 20 < total_results,
        ),
    )


@animes_router.get("/em-alta", response_model=KitsuPage[AnimeRead])
def listar_animes_em_alta(
    anime_service: AnimeServiceDep,
    paginacao: KitsuPaginationParams = Depends(),
):
    animes, total_results = anime_service.list_animes_em_alta(paginacao=paginacao)

    return KitsuPage(
        data=animes,
        pagination=KitsuPagination(
            page=paginacao.page,
            total_results=total_results,
            has_more=paginacao.page * 20 < total_results,
        ),
    )


@animes_router.get("/populares", response_model=KitsuPage[AnimeRead])
def listar_animes_populares(
    anime_service: AnimeServiceDep,
    paginacao: KitsuPaginationParams = Depends(),
):
    animes, total_results = anime_service.list_animes_populares(paginacao=paginacao)

    return KitsuPage(
        data=animes,
        pagination=KitsuPagination(
            page=paginacao.page,
            total_results=total_results,
            has_more=paginacao.page * 20 < total_results,
        ),
    )


@animes_router.get("/em-breve", response_model=KitsuPage[AnimeRead])
def listar_animes_em_breve(
    anime_service: AnimeServiceDep,
    paginacao: KitsuPaginationParams = Depends(),
):
    animes, total_results = anime_service.list_animes_em_breve(paginacao=paginacao)

    return KitsuPage(
        data=animes,
        pagination=KitsuPagination(
            page=paginacao.page,
            total_results=total_results,
            has_more=paginacao.page * 20 < total_results,
        ),
    )


@animes_router.get("/categorias", response_model=KitsuPage[CategoriaRead])
def listar_categorias(
    anime_service: AnimeServiceDep,
    paginacao: KitsuPaginationParams = Depends(),
):
    categorias, total_results = anime_service.list_categorias(paginacao=paginacao)

    return KitsuPage(
        data=categorias,
        pagination=KitsuPagination(
            page=paginacao.page,
            total_results=total_results,
            has_more=paginacao.page * 20 < total_results,
        ),
    )


@animes_router.get("/favoritos", response_model=CursorPage[AnimeFavoritoRead])
def listar_animes_favoritos(
    current_user: CurrentUsuarioDep,
    favorito_service: FavoritoServiceDep,
    paging_params: CursorMediaPaginationParams = Depends(),
):
    animes, paging = favorito_service.list_favoritos_anime(
        current_user.id,
        paging_params.cursor,
        paging_params.limit,
        paging_params.ordenacao,
    )
    return CursorPage(data=animes, pagination=paging)


@animes_router.get("/assistidos", response_model=CursorPage[AnimeAssistidoRead])
def listar_animes_assistidos(
    current_user: CurrentUsuarioDep,
    assistido_service: AssistidoServiceDep,
    paging_params: CursorMediaPaginationParams = Depends(),
):
    animes, paging = assistido_service.list_assistidos_anime(
        current_user.id,
        paging_params.cursor,
        paging_params.limit,
        paging_params.ordenacao,
    )
    return CursorPage(data=animes, pagination=paging)


@animes_router.get("/{anime_id}", response_model=AnimeRead)
def buscar_anime_id(anime_id: int, anime_service: AnimeServiceDep):
    return anime_service.get_anime(anime_id=anime_id)


@animes_router.get(
    "/{anime_id}/avaliacoes", response_model=CursorPage[AvaliacaoConteudoRead]
)
def listar_avaliacoes_do_anime(
    anime_id: int,
    avaliacao_service: AvaliacaoServiceDep,
    paging_params: CursorMediaPaginationParams = Depends(),
):
    avaliacoes, paging = avaliacao_service.list_avaliacoes_anime(
        anime_id,
        paging_params.cursor,
        paging_params.limit,
        paging_params.ordenacao,
    )
    return CursorPage(data=avaliacoes, pagination=paging)


@animes_router.post(
    "/{anime_id}/avaliacoes",
    response_model=AvaliacaoBase,
    status_code=status.HTTP_201_CREATED,
)
def criar_avaliacao_do_anime(
    anime_id: int,
    avaliacao: AvaliacaoCreate,
    current_user: CurrentUsuarioDep,
    avaliacao_service: AvaliacaoServiceDep,
):
    return avaliacao_service.create_avaliacao(
        avaliacao, anime_id, current_user.id, tipo_conteudo="anime"
    )


@animes_router.patch("/{anime_id}/avaliacoes", response_model=AvaliacaoBase)
def atualizar_avaliacao_do_anime(
    anime_id: int,
    avaliacao: AvaliacaoUpdate,
    current_user: CurrentUsuarioDep,
    avaliacao_service: AvaliacaoServiceDep,
):
    return avaliacao_service.update_avaliacao(
        avaliacao, anime_id, current_user.id, tipo_conteudo="anime"
    )


@animes_router.delete("/{anime_id}/avaliacoes", status_code=status.HTTP_204_NO_CONTENT)
def remover_avaliacao_do_anime(
    anime_id: int,
    current_user: CurrentUsuarioDep,
    avaliacao_service: AvaliacaoServiceDep,
):
    avaliacao_service.delete_avaliacao(anime_id, current_user.id, tipo_conteudo="anime")


@animes_router.post("/{anime_id}/favoritos", status_code=status.HTTP_204_NO_CONTENT)
def adicionar_anime_aos_favoritos(
    anime_id: int,
    current_user: CurrentUsuarioDep,
    favorito_service: FavoritoServiceDep,
):
    favorito_service.add_favorito_anime(anime_id, current_user.id)


@animes_router.post("/{anime_id}/assistidos", status_code=status.HTTP_204_NO_CONTENT)
def adicionar_anime_aos_assistidos(
    anime_id: int,
    current_user: CurrentUsuarioDep,
    assistido_service: AssistidoServiceDep,
):
    assistido_service.add_assistido_anime(anime_id, current_user.id)


@animes_router.delete("/{anime_id}/favoritos", status_code=status.HTTP_204_NO_CONTENT)
def remover_anime_dos_favoritos(
    anime_id: int,
    current_user: CurrentUsuarioDep,
    favorito_service: FavoritoServiceDep,
):
    favorito_service.remove_favorito_anime(anime_id, current_user.id)


@animes_router.delete("/{anime_id}/assistidos", status_code=status.HTTP_204_NO_CONTENT)
def remover_anime_dos_assistidos(
    anime_id: int,
    current_user: CurrentUsuarioDep,
    assistido_service: AssistidoServiceDep,
):
    assistido_service.remove_assistido_anime(anime_id, current_user.id)
