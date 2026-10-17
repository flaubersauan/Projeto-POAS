from typing import Annotated

from fastapi import Depends
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import contains_eager

from database import SessionDep
from models import Anime, Assistido, Usuario, Filme, Serie
from schemas.pagination.cursor import OrdenacaoCursor


class AssistidoRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def get_assistido(self, id: int) -> Assistido | None:
        return self.session.get(Assistido, id)

    def get_assistido_by_conteudo_id_and_usuario_id(
        self, conteudo_id: int, usuario_id: int
    ) -> Assistido | None:
        return self.session.scalar(
            select(Assistido).where(
                Assistido.conteudo_id == conteudo_id,
                Assistido.usuario_id == usuario_id,
            )
        )

    def get_assistidos_usuario(self, usuario: Usuario) -> list[Assistido]:
        return self.session.scalars(
            select(Assistido).where(Assistido.usuario == usuario)
        )

    def list_series_assistidas(
        self,
        usuario: Usuario,
        last_id: int,
        limit: int,
        ordenacao: OrdenacaoCursor,
    ) -> tuple[list[tuple[Serie, Assistido]], bool]:
        cursor_date = self.session.scalar(
            select(Assistido.data_adicao).where(
                Assistido.id == last_id, Assistido.usuario_id == usuario.id
            )
        )
        query = select(Serie, Assistido).select_from(Assistido)
        if cursor_date:
            operator = (
                (Assistido.data_adicao < cursor_date, Assistido.id < last_id)
                if ordenacao is OrdenacaoCursor.RECENTES
                else (Assistido.data_adicao > cursor_date, Assistido.id > last_id)
            )
            query = query.where(
                or_(
                    operator[0],
                    and_(Assistido.data_adicao == cursor_date, operator[1]),
                )
            )
        items = self.session.execute(
            query.join(Serie, Serie.conteudo_id == Assistido.conteudo_id)
            .join(Serie.conteudo)
            .options(contains_eager(Serie.conteudo))
            .where(Assistido.usuario_id == usuario.id)
            .order_by(
                (
                    Assistido.data_adicao.desc()
                    if ordenacao is OrdenacaoCursor.RECENTES
                    else Assistido.data_adicao.asc()
                ),
                (
                    Assistido.id.desc()
                    if ordenacao is OrdenacaoCursor.RECENTES
                    else Assistido.id.asc()
                ),
            )
            .limit(limit + 1)
        ).all()
        has_more = len(items) > limit
        return items[:limit], has_more

    def list_filmes_assistidos(
        self,
        usuario: Usuario,
        last_id: int,
        limit: int,
        ordenacao: OrdenacaoCursor,
    ) -> tuple[list[tuple[Filme, Assistido]], bool]:
        cursor_date = self.session.scalar(
            select(Assistido.data_adicao).where(
                Assistido.id == last_id, Assistido.usuario_id == usuario.id
            )
        )
        query = select(Filme, Assistido).select_from(Assistido)
        if cursor_date:
            operator = (
                (Assistido.data_adicao < cursor_date, Assistido.id < last_id)
                if ordenacao is OrdenacaoCursor.RECENTES
                else (Assistido.data_adicao > cursor_date, Assistido.id > last_id)
            )
            query = query.where(
                or_(
                    operator[0],
                    and_(Assistido.data_adicao == cursor_date, operator[1]),
                )
            )
        items = self.session.execute(
            query.join(Filme, Filme.conteudo_id == Assistido.conteudo_id)
            .join(Filme.conteudo)
            .options(contains_eager(Filme.conteudo))
            .where(Assistido.usuario_id == usuario.id)
            .order_by(
                (
                    Assistido.data_adicao.desc()
                    if ordenacao is OrdenacaoCursor.RECENTES
                    else Assistido.data_adicao.asc()
                ),
                (
                    Assistido.id.desc()
                    if ordenacao is OrdenacaoCursor.RECENTES
                    else Assistido.id.asc()
                ),
            )
            .limit(limit + 1)
        ).all()
        has_more = len(items) > limit
        return items[:limit], has_more

    def list_animes_assistidos(
        self,
        usuario: Usuario,
        last_id: int,
        limit: int,
        ordenacao: OrdenacaoCursor,
    ) -> tuple[list[tuple[Anime, Assistido]], bool]:
        cursor_date = self.session.scalar(
            select(Assistido.data_adicao).where(
                Assistido.id == last_id, Assistido.usuario_id == usuario.id
            )
        )
        query = select(Anime, Assistido).select_from(Assistido)
        if cursor_date:
            operator = (
                (Assistido.data_adicao < cursor_date, Assistido.id < last_id)
                if ordenacao is OrdenacaoCursor.RECENTES
                else (Assistido.data_adicao > cursor_date, Assistido.id > last_id)
            )
            query = query.where(
                or_(
                    operator[0],
                    and_(Assistido.data_adicao == cursor_date, operator[1]),
                )
            )
        items = self.session.execute(
            query.join(Anime, Anime.conteudo_id == Assistido.conteudo_id)
            .join(Anime.conteudo)
            .options(contains_eager(Anime.conteudo))
            .where(Assistido.usuario_id == usuario.id)
            .order_by(
                (
                    Assistido.data_adicao.desc()
                    if ordenacao is OrdenacaoCursor.RECENTES
                    else Assistido.data_adicao.asc()
                ),
                (
                    Assistido.id.desc()
                    if ordenacao is OrdenacaoCursor.RECENTES
                    else Assistido.id.asc()
                ),
            )
            .limit(limit + 1)
        ).all()
        has_more = len(items) > limit
        return items[:limit], has_more

    def add_assistido_serie(self, serie: Serie, usuario: Usuario) -> Assistido:
        assistido = Assistido(
            conteudo=serie.conteudo,
            usuario=usuario,
        )
        return self.create_assistido(assistido)

    def add_assistido_filme(self, filme: Filme, usuario: Usuario) -> Assistido:
        assistido = Assistido(
            conteudo=filme.conteudo,
            usuario=usuario,
        )
        return self.create_assistido(assistido)

    def add_assistido_anime(self, anime: Anime, usuario: Usuario) -> Assistido:
        assistido = Assistido(
            conteudo=anime.conteudo,
            usuario=usuario,
        )
        return self.create_assistido(assistido)

    def create_assistido(self, assistido: Assistido) -> Assistido:
        self.session.add(assistido)
        self.session.flush()
        return assistido

    def delete_assistido(self, assistido: Assistido):
        self.session.delete(assistido)
        self.session.flush()


AssistidoRepositoryDep = Annotated[AssistidoRepository, Depends(AssistidoRepository)]
