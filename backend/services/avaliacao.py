from typing import Annotated

from fastapi import Depends

from mappers.avaliacao import AvaliacaoMapper
from models.conteudo import TipoConteudo
from exceptions import ConflictException, NotFoundException
from models import Avaliacao
from repositories import AvaliacaoRepositoryDep
from schemas.avaliacao import (
    AvaliacaoConteudoRead,
    AvaliacaoUsuarioRead,
    AvaliacaoCreate,
    AvaliacaoUpdate,
)
from services.usuario import UsuarioServiceDep
from services.conteudo import ConteudoServiceDep
from services.serie import SerieServiceDep
from services.filme import FilmeServiceDep
from services.anime import AnimeServiceDep
from schemas.pagination.cursor import CursorPagination, OrdenacaoCursor


class AvaliacaoService:
    def __init__(
        self,
        avaliacao_repository: AvaliacaoRepositoryDep,
        usuario_service: UsuarioServiceDep,
        conteudo_service: ConteudoServiceDep,
        serie_service: SerieServiceDep,
        filme_service: FilmeServiceDep,
        anime_service: AnimeServiceDep,
    ):
        self.avaliacao_repository = avaliacao_repository
        self.usuario_service = usuario_service
        self.conteudo_service = conteudo_service
        self.serie_service = serie_service
        self.filme_service = filme_service
        self.anime_service = anime_service

    def list_avaliacoes_usuario(
        self,
        usuario_id: int,
        last_id: int,
        limit: int,
        ordenacao: OrdenacaoCursor,
    ) -> tuple[list[AvaliacaoUsuarioRead], CursorPagination]:
        """Retorna uma página de avaliações do usuário autenticado."""
        usuario = self.usuario_service.get_usuario(usuario_id)
        avaliacoes, has_more = self.avaliacao_repository.list_avaliacoes_by_usuario(
            usuario, last_id, limit, ordenacao
        )
        items = AvaliacaoMapper.map_avaliacoes_usuario(avaliacoes)
        return items, CursorPagination(
            cursor=avaliacoes[-1].id if avaliacoes else None,
            has_more=has_more,
        )

    def list_avaliacoes_conteudo(
        self,
        id_externo: int,
        tipo: TipoConteudo,
        last_id: int,
        limit: int,
        ordenacao: OrdenacaoCursor,
    ) -> tuple[list[AvaliacaoConteudoRead], CursorPagination]:
        conteudo = self.conteudo_service.get_conteudo_by_id_externo_and_tipo(
            id_externo, tipo
        )
        avaliacoes, has_more = self.avaliacao_repository.list_avaliacoes_by_conteudo(
            conteudo, last_id, limit, ordenacao
        )
        items = AvaliacaoMapper.map_avaliacoes_conteudo(avaliacoes)
        return items, CursorPagination(
            cursor=avaliacoes[-1].id if avaliacoes else None,
            has_more=has_more,
        )

    def list_avaliacoes_serie(
        self, serie_id: int, last_id: int, limit: int, ordenacao: OrdenacaoCursor
    ) -> tuple[list[AvaliacaoConteudoRead], CursorPagination]:
        """Retorna todas as avaliações de uma série específica."""
        return self.list_avaliacoes_conteudo(
            serie_id, tipo="serie", last_id=last_id, limit=limit, ordenacao=ordenacao
        )

    # --- Filme evaluations ---
    def list_avaliacoes_filme(
        self, filme_id: int, last_id: int, limit: int, ordenacao: OrdenacaoCursor
    ) -> tuple[list[AvaliacaoConteudoRead], CursorPagination]:
        return self.list_avaliacoes_conteudo(
            filme_id, tipo="filme", last_id=last_id, limit=limit, ordenacao=ordenacao
        )

    # --- Anime evaluations ---
    def list_avaliacoes_anime(
        self, anime_id: int, last_id: int, limit: int, ordenacao: OrdenacaoCursor
    ) -> tuple[list[AvaliacaoConteudoRead], CursorPagination]:
        return self.list_avaliacoes_conteudo(
            anime_id, tipo="anime", last_id=last_id, limit=limit, ordenacao=ordenacao
        )

    def get_avaliacao_usuario_conteudo(
        self, usuario_id: int, conteudo_id: int
    ) -> Avaliacao | None:
        """Busca uma avaliação específica do usuário para um conteúdo."""
        usuario = self.usuario_service.get_usuario(usuario_id)
        conteudo = self.conteudo_service.get_conteudo(conteudo_id)
        return self.avaliacao_repository.get_avaliacao_by_usuario_and_conteudo(
            usuario,
            conteudo,
        )

    def create_avaliacao(
        self,
        avaliacao_data: AvaliacaoCreate,
        id_externo: int,
        usuario_id: int,
        tipo_conteudo: TipoConteudo,
    ) -> Avaliacao:
        usuario = self.usuario_service.get_usuario(usuario_id)
        conteudo = self.conteudo_service.get_conteudo_by_id_externo_and_tipo(
            id_externo, tipo_conteudo
        )

        avaliacao_existente = (
            self.avaliacao_repository.get_avaliacao_by_usuario_and_conteudo(
                usuario,
                conteudo,
            )
        )
        if avaliacao_existente:
            raise ConflictException("Você já avaliou este conteúdo")

        avaliacao = Avaliacao(
            conteudo=conteudo,
            usuario=usuario,
            estrelas=avaliacao_data.estrelas,
            comentario=avaliacao_data.comentario,
        )

        return self.avaliacao_repository.create_avaliacao(avaliacao)

    def update_avaliacao(
        self,
        avaliacao_data: AvaliacaoUpdate,
        id_externo: int,
        usuario_id: int,
        tipo_conteudo: TipoConteudo,
    ) -> Avaliacao:
        usuario = self.usuario_service.get_usuario(usuario_id)
        conteudo = self.conteudo_service.get_conteudo_by_id_externo_and_tipo(
            id_externo, tipo_conteudo
        )

        avaliacao = self.avaliacao_repository.get_avaliacao_by_usuario_and_conteudo(
            usuario,
            conteudo,
        )
        if not avaliacao:
            raise NotFoundException(
                "Avaliação do conteúdo não encontrada para o usuário atual"
            )

        if avaliacao_data.estrelas is not None:
            avaliacao.estrelas = avaliacao_data.estrelas
        if avaliacao_data.comentario is not None:
            avaliacao.comentario = avaliacao_data.comentario

        return self.avaliacao_repository.update_avaliacao(avaliacao)

    def delete_avaliacao(
        self, id_externo: int, usuario_id: int, tipo_conteudo: TipoConteudo
    ):
        usuario = self.usuario_service.get_usuario(usuario_id)
        conteudo = self.conteudo_service.get_conteudo_by_id_externo_and_tipo(
            id_externo, tipo_conteudo
        )

        avaliacao = self.avaliacao_repository.get_avaliacao_by_usuario_and_conteudo(
            usuario,
            conteudo,
        )
        if not avaliacao:
            raise NotFoundException(
                "Avaliação do conteúdo não encontrada para o usuário atual"
            )

        self.avaliacao_repository.delete_avaliacao(avaliacao)


AvaliacaoServiceDep = Annotated[AvaliacaoService, Depends(AvaliacaoService)]
