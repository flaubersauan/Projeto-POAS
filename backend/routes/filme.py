from fastapi import APIRouter, Depends, status

from auth.dependencies import CurrentUsuarioDep
from schemas.pagination.tmdb import TmdbPage, TmdbPagination, TmdbPaginationParams
from schemas.filme import FilmeFiltros, FilmeListRead, FilmeRead, GeneroFilme
from schemas.favorito import FilmeFavoritoRead
from schemas.assistido import FilmeAssistidoRead
from services import AssistidoServiceDep, FilmeServiceDep, AvaliacaoServiceDep
from services.favorito import FavoritoServiceDep
from schemas.avaliacao import (
    AvaliacaoCreate,
    AvaliacaoFilmeRead,
    AvaliacaoUpdate,
)

filmes_router = APIRouter(prefix="/filmes", tags=["filmes"])


@filmes_router.get("", response_model=TmdbPage[FilmeListRead])
def buscar_filmes(
    filme_service: FilmeServiceDep,
    filtros: FilmeFiltros = Depends(FilmeFiltros.as_dependency),
    busca: str | None = None,
    paginacao: TmdbPaginationParams = Depends()
):
    filmes, total_pages, total_results = filme_service.search_filmes(
        busca=busca,
        filtros=filtros,
        page=paginacao.page,
    )

    return TmdbPage(
        data=filmes,
        pagination=TmdbPagination(
            page=paginacao.page,
            total_pages=total_pages,
            total_results=total_results,
            has_more=paginacao.page < total_pages
        )
    )


@filmes_router.get("/em-alta", response_model=TmdbPage[FilmeListRead])
def listar_filmes_em_alta(
    filme_service: FilmeServiceDep,
    paginacao: TmdbPaginationParams = Depends(),
):
    filmes, total_pages, total_results = filme_service.list_filmes_em_alta(
        page=paginacao.page,
    )

    return TmdbPage(
        data=filmes,
        pagination=TmdbPagination(
            page=paginacao.page,
            total_pages=total_pages,
            total_results=total_results,
            has_more=paginacao.page < total_pages
        )
    )


@filmes_router.get("/populares", response_model=TmdbPage[FilmeListRead])
def listar_filmes_populares(
    filme_service: FilmeServiceDep,
    paginacao: TmdbPaginationParams = Depends(),
):
    filmes, total_pages, total_results = filme_service.list_filmes_populares(
        page=paginacao.page,
    )

    return TmdbPage(
        data=filmes,
        pagination=TmdbPagination(
            page=paginacao.page,
            total_pages=total_pages,
            total_results=total_results,
            has_more=paginacao.page < total_pages,
        ),
    )


@filmes_router.get("/em-breve", response_model=TmdbPage[FilmeListRead])
def listar_filmes_em_breve(
    filme_service: FilmeServiceDep,
    paginacao: TmdbPaginationParams = Depends(),
):
    filmes, total_pages, total_results = filme_service.list_filmes_em_breve(
        page=paginacao.page,
    )

    return TmdbPage(
        data=filmes,
        pagination=TmdbPagination(
            page=paginacao.page,
            total_pages=total_pages,
            total_results=total_results,
            has_more=paginacao.page < total_pages,
        ),
    )


@filmes_router.get("/generos", response_model=list[GeneroFilme])
def listar_generos_filmes(filme_service: FilmeServiceDep):
    return filme_service.list_generos()


@filmes_router.get("/favoritos", response_model=list[FilmeFavoritoRead])
def listar_filmes_favoritos(
    current_user: CurrentUsuarioDep,
    favorito_service: FavoritoServiceDep,
):
    return favorito_service.list_favoritos_filme(current_user.id)


@filmes_router.get("/assistidos", response_model=list[FilmeAssistidoRead])
def listar_filmes_assistidos(
    current_user: CurrentUsuarioDep,
    assistido_service: AssistidoServiceDep,
):
    return assistido_service.list_assistidos_filme(current_user.id)


@filmes_router.get("/{filme_id}", response_model=FilmeRead)
def buscar_filme_id(filme_id: int, filme_service: FilmeServiceDep):
    return filme_service.get_filme(filme_id=filme_id)


@filmes_router.get("/{filme_id}/avaliacoes", response_model=list[AvaliacaoFilmeRead])
def listar_avaliacoes_do_filme(
    filme_id: int,
    avaliacao_service: AvaliacaoServiceDep,
):
    return avaliacao_service.list_avaliacoes_filme(filme_id)


@filmes_router.post(
    "/{filme_id}/avaliacoes",
    response_model=AvaliacaoFilmeRead,
    status_code=status.HTTP_201_CREATED,
)
def criar_avaliacao_do_filme(
    filme_id: int,
    avaliacao: AvaliacaoCreate,
    current_user: CurrentUsuarioDep,
    avaliacao_service: AvaliacaoServiceDep,
):
    return avaliacao_service.create_avaliacao_filme(filme_id, current_user.id, avaliacao)


@filmes_router.patch("/{filme_id}/avaliacoes", response_model=AvaliacaoFilmeRead)
def atualizar_avaliacao_do_filme(
    filme_id: int,
    avaliacao: AvaliacaoUpdate,
    current_user: CurrentUsuarioDep,
    avaliacao_service: AvaliacaoServiceDep,
):
    return avaliacao_service.update_avaliacao_filme(filme_id, current_user.id, avaliacao)


@filmes_router.delete("/{filme_id}/avaliacoes", status_code=status.HTTP_204_NO_CONTENT)
def remover_avaliacao_do_filme(
    filme_id: int,
    current_user: CurrentUsuarioDep,
    avaliacao_service: AvaliacaoServiceDep,
):
    avaliacao_service.delete_avaliacao_filme(filme_id, current_user.id)


@filmes_router.post("/{filme_id}/favoritos", status_code=status.HTTP_204_NO_CONTENT)
def adicionar_filme_aos_favoritos(
    filme_id: int,
    current_user: CurrentUsuarioDep,
    favorito_service: FavoritoServiceDep,
):
    favorito_service.add_favorito_filme(filme_id, current_user.id)


@filmes_router.post("/{filme_id}/assistidos", status_code=status.HTTP_204_NO_CONTENT)
def adicionar_filme_aos_assistidos(
    filme_id: int,
    current_user: CurrentUsuarioDep,
    assistido_service: AssistidoServiceDep,
):
    assistido_service.add_assistido_filme(filme_id, current_user.id)


@filmes_router.delete("/{filme_id}/favoritos", status_code=status.HTTP_204_NO_CONTENT)
def remover_filme_dos_favoritos(
    filme_id: int,
    current_user: CurrentUsuarioDep,
    favorito_service: FavoritoServiceDep,
):
    favorito_service.remove_favorito_filme(filme_id, current_user.id)


@filmes_router.delete("/{filme_id}/assistidos", status_code=status.HTTP_204_NO_CONTENT)
def remover_filme_dos_assistidos(
    filme_id: int,
    current_user: CurrentUsuarioDep,
    assistido_service: AssistidoServiceDep,
):
    assistido_service.remove_assistido_filme(filme_id, current_user.id)
