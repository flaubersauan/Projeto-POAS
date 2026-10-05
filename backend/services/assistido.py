from typing import Annotated

from fastapi import Depends

from mappers.assistido import AssistidoMapper
from exceptions import ConflictException, EntityNotFoundException, NotFoundException
from models import Assistido
from repositories import AssistidoRepositoryDep
from schemas.assistido import AnimeAssistidoRead, FilmeAssistidoRead, SerieAssistidaRead
from .usuario import UsuarioServiceDep
from .serie import SerieServiceDep
from .filme import FilmeServiceDep
from .anime import AnimeServiceDep


class AssistidoService:
    def __init__(
        self,
        assistido_repository: AssistidoRepositoryDep,
        usuario_service: UsuarioServiceDep,
        serie_service: SerieServiceDep,
        filme_service: FilmeServiceDep,
        anime_service: AnimeServiceDep,
    ):
        self.assistido_repository = assistido_repository
        self.usuario_service = usuario_service
        self.serie_service = serie_service
        self.filme_service = filme_service
        self.anime_service = anime_service

    def get_assistido(self, assistido_id: int) -> Assistido:
        assistido = self.assistido_repository.get_assistido(assistido_id)
        if not assistido:
            raise EntityNotFoundException("Assistido", assistido_id)
        return assistido

    def list_assistidos_serie(self, usuario_id: int) -> list[SerieAssistidaRead]:
        usuario = self.usuario_service.get_usuario(usuario_id)
        return AssistidoMapper.map_series(
            self.assistido_repository.list_series_assistidas(usuario)
        )

    def list_assistidos_filme(self, usuario_id: int) -> list[FilmeAssistidoRead]:
        usuario = self.usuario_service.get_usuario(usuario_id)
        return AssistidoMapper.map_filmes(
            self.assistido_repository.list_filmes_assistidos(usuario)
        )

    def list_assistidos_anime(self, usuario_id: int) -> list[AnimeAssistidoRead]:
        usuario = self.usuario_service.get_usuario(usuario_id)
        return AssistidoMapper.map_animes(
            self.assistido_repository.list_animes_assistidos(usuario)
        )

    def add_assistido_serie(self, serie_id: int, usuario_id: int):
        usuario = self.usuario_service.get_usuario(usuario_id)
        serie = self.serie_service.get_serie_from_db(serie_id)
        if not serie:
            result = self.serie_service.get_serie_from_api_and_update_database(serie_id)
            _, serie = result

        if self.assistido_repository.get_assistido_by_conteudo_id_and_usuario_id(
            serie.conteudo_id, usuario.id
        ):
            raise ConflictException("A série já está na lista de assistidos")

        self.assistido_repository.add_assistido_serie(serie, usuario)

    def add_assistido_filme(self, filme_id: int, usuario_id: int):
        usuario = self.usuario_service.get_usuario(usuario_id)
        filme = self.filme_service.get_filme_from_db(filme_id)
        if not filme:
            _, filme = self.filme_service.get_filme_from_api_and_update_database(filme_id)
            filme = self.filme_service.get_filme_from_db(filme_id)

        if not filme:
            raise EntityNotFoundException("Filme", filme_id)

        if self.assistido_repository.get_assistido_by_conteudo_id_and_usuario_id(
            filme.conteudo_id, usuario.id
        ):
            raise ConflictException("O filme já está na lista de assistidos")

        self.assistido_repository.add_assistido_filme(filme, usuario)

    def add_assistido_anime(self, anime_id: int, usuario_id: int):
        usuario = self.usuario_service.get_usuario(usuario_id)
        anime = self.anime_service.get_anime_from_db(anime_id)
        if not anime:
            _, anime = self.anime_service.get_anime_from_api_and_update_database(anime_id)

        if self.assistido_repository.get_assistido_by_conteudo_id_and_usuario_id(
            anime.conteudo_id, usuario.id
        ):
            raise ConflictException("O anime já está na lista de assistidos")

        self.assistido_repository.add_assistido_anime(anime, usuario)

    def remove_assistido_serie(self, serie_id: int, usuario_id: int):
        usuario = self.usuario_service.get_usuario(usuario_id)
        serie = self.serie_service.get_serie_from_db(serie_id)
        if not serie:
            raise EntityNotFoundException("Série", serie_id)

        assistido = self.assistido_repository.get_assistido_by_conteudo_id_and_usuario_id(
            conteudo_id=serie.conteudo_id,
            usuario_id=usuario.id,
        )

        if not assistido:
            raise NotFoundException("Série não encontrada na lista de assistidos")

        self.assistido_repository.delete_assistido(assistido)

    def remove_assistido_filme(self, filme_id: int, usuario_id: int):
        usuario = self.usuario_service.get_usuario(usuario_id)
        filme = self.filme_service.get_filme_from_db(filme_id)
        if not filme:
            raise EntityNotFoundException("Filme", filme_id)

        assistido = self.assistido_repository.get_assistido_by_conteudo_id_and_usuario_id(
            conteudo_id=filme.conteudo_id,
            usuario_id=usuario.id,
        )

        if not assistido:
            raise NotFoundException("Filme não encontrado na lista de assistidos")

        self.assistido_repository.delete_assistido(assistido)

    def remove_assistido_anime(self, anime_id: int, usuario_id: int):
        usuario = self.usuario_service.get_usuario(usuario_id)
        anime = self.anime_service.get_anime_from_db(anime_id)
        if not anime:
            raise EntityNotFoundException("Anime", anime_id)

        assistido = self.assistido_repository.get_assistido_by_conteudo_id_and_usuario_id(
            conteudo_id=anime.conteudo_id,
            usuario_id=usuario.id,
        )

        if not assistido:
            raise NotFoundException("Anime não encontrado na lista de assistidos")

        self.assistido_repository.delete_assistido(assistido)


AssistidoServiceDep = Annotated[AssistidoService, Depends(AssistidoService)]
