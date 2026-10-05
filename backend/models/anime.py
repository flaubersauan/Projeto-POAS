from typing import Optional, TYPE_CHECKING
from sqlalchemy import ForeignKey, DateTime, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date

from utils import get_now_datetime_utc
from .base import Base

if TYPE_CHECKING:
    from .conteudo import Conteudo


class Anime(Base):
    """Representa os dados de um anime associado a um conteudo.

    Args:
        conteudo_id: Identificador do conteudo associado e chave primaria.
        titulo: Titulo canonico do anime.
        titulo_original: Titulo original do anime (ja_jp/en_jp do Kitsu).
        status: Status atual do anime.
        capa: URL completa da imagem de capa no Kitsu, quando houver.
        banner: URL completa da imagem de banner no Kitsu, quando houver.
        data_lancamento: Data de inicio de exibicao do anime, quando conhecida.
        data_atualizacao: Data e hora da ultima atualizacao dos dados.
        conteudo: Relacionamento com o conteudo associado.
    """

    __tablename__ = "anime"

    conteudo_id: Mapped[int] = mapped_column(ForeignKey("conteudo.id"), primary_key=True)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    titulo_original: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False)
    # Kitsu retorna URLs completas, por isso 512 em vez de 255
    capa: Mapped[Optional[str]] = mapped_column(String(512))
    banner: Mapped[Optional[str]] = mapped_column(String(512))
    data_lancamento: Mapped[Optional[date]] = mapped_column(Date)
    data_atualizacao: Mapped[datetime] = mapped_column(DateTime(timezone=True), insert_default=get_now_datetime_utc, onupdate=get_now_datetime_utc, nullable=False)

    conteudo: Mapped["Conteudo"] = relationship(back_populates="anime")
