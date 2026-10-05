from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import contains_eager

from database import SessionDep
from models import Anime, Favorito, Usuario, Conteudo, Filme, Serie


class FavoritoRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def get_favorito(self, id: int) -> Favorito | None:
        return self.session.get(Favorito, id)

    def get_favorito_by_conteudo_id_and_usuario_id(self, conteudo_id: int, usuario_id: int) -> Favorito | None:
        return self.session.scalar(
            select(Favorito)
            .where(
                Favorito.conteudo_id == conteudo_id,
                Favorito.usuario_id == usuario_id
            )
        )

    def get_favoritos_usuario(self, usuario: Usuario) -> list[Favorito]:
        return self.session.scalars(
            select(Favorito)
            .where(
                Favorito.usuario == usuario
            )
        )

    def list_series_favoritas(self, usuario: Usuario) -> list[tuple[Serie, Favorito]]:
        return self.session.execute(
            select(Serie, Favorito)
            .select_from(Favorito)
            .join(Serie, Serie.conteudo_id == Favorito.conteudo_id)
            .join(Serie.conteudo)
            .options(contains_eager(Serie.conteudo))
            .where(Favorito.usuario == usuario)
        ).all()

    def list_filmes_favoritos(self, usuario: Usuario) -> list[tuple[Filme, Favorito]]:
        return self.session.execute(
            select(Filme, Favorito)
            .select_from(Favorito)
            .join(Filme, Filme.conteudo_id == Favorito.conteudo_id)
            .join(Filme.conteudo)
            .options(contains_eager(Filme.conteudo))
            .where(Favorito.usuario == usuario)
        ).all()

    def list_animes_favoritos(self, usuario: Usuario) -> list[tuple[Anime, Favorito]]:
        return self.session.execute(
            select(Anime, Favorito)
            .select_from(Favorito)
            .join(Anime, Anime.conteudo_id == Favorito.conteudo_id)
            .join(Anime.conteudo)
            .options(contains_eager(Anime.conteudo))
            .where(Favorito.usuario == usuario)
        ).all()

    def add_favorito_serie(self, serie: Serie, usuario: Usuario) -> Favorito:
        favorito = Favorito(
            conteudo=serie.conteudo,
            usuario=usuario,
        )
        return self.create_favorito(favorito)

    def add_favorito_filme(self, filme: Filme, usuario: Usuario) -> Favorito:
        favorito = Favorito(
            conteudo=filme.conteudo,
            usuario=usuario,
        )
        return self.create_favorito(favorito)

    def add_favorito_anime(self, anime: Anime, usuario: Usuario) -> Favorito:
        favorito = Favorito(
            conteudo=anime.conteudo,
            usuario=usuario,
        )
        return self.create_favorito(favorito)

    def create_favorito(self, favorito: Favorito) -> Favorito:
        self.session.add(favorito)
        self.session.flush()
        return favorito

    def delete_favorito(self, favorito: Favorito):
        self.session.delete(favorito)
        self.session.flush()


FavoritoRepositoryDep = Annotated[
    FavoritoRepository, Depends(FavoritoRepository)
]
