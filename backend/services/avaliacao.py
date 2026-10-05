from typing import Annotated

from fastapi import Depends

from exceptions import ConflictException, NotFoundException
from models import Avaliacao
from repositories import AvaliacaoRepositoryDep
from schemas.avaliacao import AvaliacaoCreate, AvaliacaoUpdate
from services.usuario import UsuarioServiceDep
from services.conteudo import ConteudoServiceDep
from services.serie import SerieServiceDep


class AvaliacaoService:
    def __init__(
        self,
        avaliacao_repository: AvaliacaoRepositoryDep,
        usuario_service: UsuarioServiceDep,
        conteudo_service: ConteudoServiceDep,
        serie_service: SerieServiceDep,
    ):
        self.avaliacao_repository = avaliacao_repository
        self.usuario_service = usuario_service
        self.conteudo_service = conteudo_service
        self.serie_service = serie_service

    def list_avaliacoes_usuario(self, usuario_id: int) -> list[Avaliacao]:
        """Retorna as avaliações do usuário autenticado."""
        usuario = self.usuario_service.get_usuario(usuario_id)
        return self.avaliacao_repository.list_avaliacoes_by_usuario(usuario)

    def list_avaliacoes_conteudo(self, serie_id: int) -> list[Avaliacao]:
        """Retorna todas as avaliações de uma série específica."""
        serie = self.serie_service.get_serie_from_db(serie_id)
        if not serie:
            _, serie = self.serie_service.get_serie_from_api_and_update_database(serie_id)

        return self.avaliacao_repository.list_avaliacoes_by_conteudo(serie.conteudo)

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
        self, serie_id: int, usuario_id: int, avaliacao_data: AvaliacaoCreate
    ) -> Avaliacao:
        usuario = self.usuario_service.get_usuario(usuario_id)
        serie = self.serie_service.get_serie_from_db(serie_id)
        if not serie:
            _, serie = self.serie_service.get_serie_from_api_and_update_database(serie_id)

        avaliacao_existente = self.avaliacao_repository.get_avaliacao_by_usuario_and_conteudo(
            usuario,
            serie.conteudo,
        )
        if avaliacao_existente:
            raise ConflictException("Você já avaliou esta série")

        avaliacao = Avaliacao(
            conteudo=serie.conteudo,
            usuario=usuario,
            estrelas=avaliacao_data.estrelas,
            comentario=avaliacao_data.comentario,
        )
        return self.avaliacao_repository.create_avaliacao(avaliacao)

    def update_avaliacao(
        self, serie_id: int, usuario_id: int, avaliacao_data: AvaliacaoUpdate
    ) -> Avaliacao:
        usuario = self.usuario_service.get_usuario(usuario_id)
        serie = self.serie_service.get_serie_from_db(serie_id)
        if not serie:
            _, serie = self.serie_service.get_serie_from_api_and_update_database(serie_id)

        avaliacao = self.avaliacao_repository.get_avaliacao_by_usuario_and_conteudo(
            usuario,
            serie.conteudo,
        )
        if not avaliacao:
            raise NotFoundException("Avaliação da série não encontrada para o usuário atual")

        if avaliacao_data.estrelas is not None:
            avaliacao.estrelas = avaliacao_data.estrelas
        if avaliacao_data.comentario is not None:
            avaliacao.comentario = avaliacao_data.comentario

        return self.avaliacao_repository.update_avaliacao(avaliacao)

    def delete_avaliacao(self, serie_id: int, usuario_id: int):
        usuario = self.usuario_service.get_usuario(usuario_id)
        serie = self.serie_service.get_serie_from_db(serie_id)
        if not serie:
            _, serie = self.serie_service.get_serie_from_api_and_update_database(serie_id)

        avaliacao = self.avaliacao_repository.get_avaliacao_by_usuario_and_conteudo(
            usuario,
            serie.conteudo,
        )
        if not avaliacao:
            raise NotFoundException("Avaliação da série não encontrada para o usuário atual")

        self.avaliacao_repository.delete_avaliacao(avaliacao)


AvaliacaoServiceDep = Annotated[AvaliacaoService, Depends(AvaliacaoService)]
