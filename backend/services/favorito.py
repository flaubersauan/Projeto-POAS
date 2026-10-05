from typing import Annotated

from fastapi import Depends

from mappers.favorito import FavoritoMapper
from exceptions import ConflictException, EntityNotFoundException, NotFoundException
from models import Favorito
from repositories import FavoritoRepositoryDep
from schemas.favorito import AnimeFavoritoRead, FilmeFavoritoRead, SerieFavoritaRead
from .usuario import UsuarioServiceDep
from .serie import SerieServiceDep
from .filme import FilmeServiceDep
from .anime import AnimeServiceDep


class FavoritoService:
    def __init__(
        self,
        favorito_repository: FavoritoRepositoryDep,
        usuario_service: UsuarioServiceDep,
        serie_service: SerieServiceDep,
        filme_service: FilmeServiceDep,
        anime_service: AnimeServiceDep,
    ):
        self.favorito_repository = favorito_repository
        self.usuario_service = usuario_service
        self.serie_service = serie_service
        self.filme_service = filme_service
        self.anime_service = anime_service

    def get_favorito(self, favorito_id: int) -> Favorito:
        favorito = self.favorito_repository.get_favorito(favorito_id)
        if not favorito:
            raise EntityNotFoundException("Favorito", favorito_id)
        return favorito

    def list_favoritos_serie(self, usuario_id: int) -> list[SerieFavoritaRead]:
        usuario = self.usuario_service.get_usuario(usuario_id)

        return FavoritoMapper.map_series(self.favorito_repository.list_series_favoritas(usuario))

    def list_favoritos_filme(self, usuario_id: int) -> list[FilmeFavoritoRead]:
        usuario = self.usuario_service.get_usuario(usuario_id)

        return FavoritoMapper.map_filmes(self.favorito_repository.list_filmes_favoritos(usuario))

    def list_favoritos_anime(self, usuario_id: int) -> list[AnimeFavoritoRead]:
        usuario = self.usuario_service.get_usuario(usuario_id)

        return FavoritoMapper.map_animes(self.favorito_repository.list_animes_favoritos(usuario))

    def add_favorito_serie(self, serie_id: int, usuario_id: int):
        usuario = self.usuario_service.get_usuario(usuario_id)
        serie = self.serie_service.get_serie_from_db(serie_id)
        if not serie:
            result = self.serie_service.get_serie_from_api_and_update_database(serie_id)
            _, serie = result

        if self.favorito_repository.get_favorito_by_conteudo_id_and_usuario_id(serie.conteudo_id, usuario.id):
            raise ConflictException("A série já está na lista de favoritos")

        self.favorito_repository.add_favorito_serie(serie, usuario)

    def add_favorito_filme(self, filme_id: int, usuario_id: int):
        usuario = self.usuario_service.get_usuario(usuario_id)
        filme = self.filme_service.get_filme_from_db(filme_id)
        if not filme:
            _, filme = self.filme_service.get_filme_from_api_and_update_database(filme_id)
            filme = self.filme_service.get_filme_from_db(filme_id)

        if not filme:
            raise EntityNotFoundException("Filme", filme_id)

        if self.favorito_repository.get_favorito_by_conteudo_id_and_usuario_id(filme.conteudo_id, usuario.id):
            raise ConflictException("O filme já está na lista de favoritos")

        self.favorito_repository.add_favorito_filme(filme, usuario)

    def add_favorito_anime(self, anime_id: int, usuario_id: int):
        usuario = self.usuario_service.get_usuario(usuario_id)
        anime = self.anime_service.get_anime_from_db(anime_id)
        if not anime:
            _, anime = self.anime_service.get_anime_from_api_and_update_database(anime_id)

        if self.favorito_repository.get_favorito_by_conteudo_id_and_usuario_id(anime.conteudo_id, usuario.id):
            raise ConflictException("O anime já está na lista de favoritos")

        self.favorito_repository.add_favorito_anime(anime, usuario)

    def remove_favorito_serie(self, serie_id: int, usuario_id: int):
        usuario = self.usuario_service.get_usuario(usuario_id)
        serie = self.serie_service.get_serie_from_db(serie_id)
        if not serie:
            raise EntityNotFoundException("Série", serie_id)

        favorito = self.favorito_repository.get_favorito_by_conteudo_id_and_usuario_id(
            conteudo_id=serie.conteudo_id,
            usuario_id=usuario.id
        )

        if not favorito:
            raise NotFoundException("Série não encontrada nos favoritos")

        self.favorito_repository.delete_favorito(favorito)

    def remove_favorito_filme(self, filme_id: int, usuario_id: int):
        usuario = self.usuario_service.get_usuario(usuario_id)
        filme = self.filme_service.get_filme_from_db(filme_id)
        if not filme:
            raise EntityNotFoundException("Filme", filme_id)

        favorito = self.favorito_repository.get_favorito_by_conteudo_id_and_usuario_id(
            conteudo_id=filme.conteudo_id,
            usuario_id=usuario.id,
        )

        if not favorito:
            raise NotFoundException("Filme não encontrado nos favoritos")

        self.favorito_repository.delete_favorito(favorito)

    def remove_favorito_anime(self, anime_id: int, usuario_id: int):
        usuario = self.usuario_service.get_usuario(usuario_id)
        anime = self.anime_service.get_anime_from_db(anime_id)
        if not anime:
            raise EntityNotFoundException("Anime", anime_id)

        favorito = self.favorito_repository.get_favorito_by_conteudo_id_and_usuario_id(
            conteudo_id=anime.conteudo_id,
            usuario_id=usuario.id,
        )

        if not favorito:
            raise NotFoundException("Anime não encontrado nos favoritos")

        self.favorito_repository.delete_favorito(favorito)


FavoritoServiceDep = Annotated[FavoritoService, Depends(FavoritoService)]
