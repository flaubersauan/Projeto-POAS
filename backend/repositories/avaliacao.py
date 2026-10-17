from typing import Annotated

from fastapi import Depends
from sqlalchemy import and_, or_, select

from database import SessionDep
from models import Avaliacao, Usuario, Conteudo
from schemas.pagination.cursor import OrdenacaoCursor


class AvaliacaoRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def list_avaliacoes_by_usuario(
        self,
        usuario: Usuario,
        last_id: int,
        limit: int,
        ordenacao: OrdenacaoCursor,
    ) -> tuple[list[Avaliacao], bool]:
        """Retorna uma página de avaliações de um usuário específico."""
        cursor_date = self.session.scalar(
            select(Avaliacao.data_criacao).where(
                Avaliacao.id == last_id, Avaliacao.usuario_id == usuario.id
            )
        )
        query = select(Avaliacao)
        if cursor_date:
            operator = (
                (Avaliacao.data_criacao < cursor_date, Avaliacao.id < last_id)
                if ordenacao is OrdenacaoCursor.RECENTES
                else (Avaliacao.data_criacao > cursor_date, Avaliacao.id > last_id)
            )
            query = query.where(
                or_(
                    operator[0],
                    and_(Avaliacao.data_criacao == cursor_date, operator[1]),
                )
            )
        avaliacoes = self.session.scalars(
            query.where(Avaliacao.usuario_id == usuario.id)
            .order_by(
                (
                    Avaliacao.data_criacao.desc()
                    if ordenacao is OrdenacaoCursor.RECENTES
                    else Avaliacao.data_criacao.asc()
                ),
                (
                    Avaliacao.id.desc()
                    if ordenacao is OrdenacaoCursor.RECENTES
                    else Avaliacao.id.asc()
                ),
            )
            .limit(limit + 1)
        ).all()
        has_more = len(avaliacoes) > limit
        return avaliacoes[:limit], has_more

    def list_avaliacoes_by_conteudo(
        self,
        conteudo: Conteudo,
        last_id: int,
        limit: int,
        ordenacao: OrdenacaoCursor,
    ) -> tuple[list[Avaliacao], bool]:
        """Retorna uma página de avaliações de um conteúdo específico."""
        cursor_date = self.session.scalar(
            select(Avaliacao.data_criacao).where(
                Avaliacao.id == last_id, Avaliacao.conteudo_id == conteudo.id
            )
        )
        query = select(Avaliacao)
        if cursor_date:
            operator = (
                (Avaliacao.data_criacao < cursor_date, Avaliacao.id < last_id)
                if ordenacao is OrdenacaoCursor.RECENTES
                else (Avaliacao.data_criacao > cursor_date, Avaliacao.id > last_id)
            )
            query = query.where(
                or_(
                    operator[0],
                    and_(Avaliacao.data_criacao == cursor_date, operator[1]),
                )
            )
        avaliacoes = self.session.scalars(
            query.where(Avaliacao.conteudo_id == conteudo.id)
            .order_by(
                (
                    Avaliacao.data_criacao.desc()
                    if ordenacao is OrdenacaoCursor.RECENTES
                    else Avaliacao.data_criacao.asc()
                ),
                (
                    Avaliacao.id.desc()
                    if ordenacao is OrdenacaoCursor.RECENTES
                    else Avaliacao.id.asc()
                ),
            )
            .limit(limit + 1)
        ).all()
        has_more = len(avaliacoes) > limit
        return avaliacoes[:limit], has_more

    def get_avaliacao_by_usuario_and_conteudo(
        self, usuario: Usuario, conteudo: Conteudo
    ) -> Avaliacao | None:
        """Busca uma avaliação específica do usuário para um conteúdo."""
        return self.session.scalar(
            select(Avaliacao).where(
                Avaliacao.usuario_id == usuario.id,
                Avaliacao.conteudo_id == conteudo.id,
            )
        )

    def create_avaliacao(self, avaliacao: Avaliacao) -> Avaliacao:
        self.session.add(avaliacao)
        self.session.flush()
        return avaliacao

    def update_avaliacao(self, avaliacao: Avaliacao) -> Avaliacao:
        self.session.flush()
        return avaliacao

    def delete_avaliacao(self, avaliacao: Avaliacao):
        self.session.delete(avaliacao)
        self.session.flush()


AvaliacaoRepositoryDep = Annotated[AvaliacaoRepository, Depends(AvaliacaoRepository)]
