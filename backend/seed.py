"""Popula o banco com dados fictícios compatíveis com o modelo atual.

Exemplos:
    python seed.py --usuarios 1000 --conteudos 2000
    python seed.py --usuarios 100 --conteudos 200 --avaliacoes 500 --seed 42
    python seed.py --reset --usuarios 1000 --conteudos 2000

As quantidades são totais por entidade nesta execução. O script preserva os
dados existentes por padrão; use ``--reset`` apenas quando quiser recriar a
massa de dados.
"""

import argparse
import random
import sys
import time
from decimal import Decimal
from typing import TypeVar

from faker import Faker
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from auth.utils import get_password_hash
from database import SessionFactory
from models import (
    Anime,
    Assistido,
    Avaliacao,
    Conteudo,
    Favorito,
    Filme,
    Serie,
    Usuario,
)
from models.conteudo import ApiFonte, TipoConteudo

fake = Faker("pt_BR")

SENHA_PADRAO = get_password_hash("12345678")
TIPOS_CONTEUDO = tuple(TipoConteudo)
VALORES_ESTRELAS = tuple(Decimal(str(valor / 2)) for valor in range(2, 11))

ModelT = TypeVar("ModelT")


def _limitar_texto(texto: str, limite: int) -> str:
    return texto[:limite]


def _imprimir_progresso(rotulo: str, atual: int, total: int, inicio: float) -> None:
    if total <= 0:
        return

    percentual = (atual / total) * 100
    decorrido = time.perf_counter() - inicio
    sys.stdout.write(
        f"\r{rotulo}: {atual}/{total} ({percentual:5.1f}%) - {decorrido:,.1f}s"
    )
    sys.stdout.flush()
    if atual >= total:
        sys.stdout.write("\n")
        sys.stdout.flush()


def _salvar_lote(session: Session, objetos: list[object]) -> None:
    session.add_all(objetos)
    session.flush()
    session.commit()


def _obter_ids(session: Session, modelo: type[ModelT]) -> list[int]:
    return list(session.scalars(select(modelo.id).order_by(modelo.id)).all())  # type: ignore[attr-defined]


def _limpar_banco(session: Session) -> None:
    for modelo in (
        Avaliacao,
        Favorito,
        Assistido,
        Filme,
        Serie,
        Anime,
        Conteudo,
        Usuario,
    ):
        session.execute(delete(modelo))
    session.commit()


def _criar_detalhe_conteudo(conteudo: Conteudo) -> Filme | Serie | Anime:
    titulo = _limitar_texto(fake.sentence(nb_words=4).rstrip("."), 255)
    titulo_original = _limitar_texto(fake.sentence(nb_words=4).rstrip("."), 255)
    status = random.choice(("Em andamento", "Concluído", "Cancelado"))
    data_lancamento = fake.date_between(start_date="-30y", end_date="today")

    if conteudo.tipo is TipoConteudo.FILME:
        return Filme(
            conteudo=conteudo,
            titulo=titulo,
            titulo_original=titulo_original,
            status=status,
            capa=f"https://picsum.photos/seed/filme-{conteudo.id_externo}/500/750",
            banner=f"https://picsum.photos/seed/filme-banner-{conteudo.id_externo}/1280/720",
            data_lancamento=data_lancamento,
        )
    if conteudo.tipo is TipoConteudo.SERIE:
        return Serie(
            conteudo=conteudo,
            titulo=titulo,
            titulo_original=titulo_original,
            status=status,
            capa=f"https://picsum.photos/seed/serie-{conteudo.id_externo}/500/750",
            banner=f"https://picsum.photos/seed/serie-banner-{conteudo.id_externo}/1280/720",
            data_lancamento=data_lancamento,
        )
    return Anime(
        conteudo=conteudo,
        titulo=titulo,
        titulo_original=titulo_original,
        status=status,
        capa=f"https://picsum.photos/seed/anime-{conteudo.id_externo}/500/750",
        banner=f"https://picsum.photos/seed/anime-banner-{conteudo.id_externo}/1280/720",
        data_lancamento=data_lancamento,
    )


def popular_usuarios(session: Session, quantidade: int, tamanho_lote: int) -> list[int]:
    if quantidade <= 0:
        return _obter_ids(session, Usuario)

    proximo_id = (session.scalar(select(func.max(Usuario.id))) or 0) + 1
    lote: list[Usuario] = []
    inicio = time.perf_counter()
    for indice in range(quantidade):
        numero = proximo_id + indice
        lote.append(
            Usuario(
                nome=_limitar_texto(fake.name(), 50),
                email=f"usuario.seed.{numero}@example.com",
                senha_hash=SENHA_PADRAO,
            )
        )
        if len(lote) == tamanho_lote or indice == quantidade - 1:
            _salvar_lote(session, lote)
            lote = []
            _imprimir_progresso("Usuários", indice + 1, quantidade, inicio)
    return _obter_ids(session, Usuario)


def popular_conteudos(
    session: Session, quantidade: int, tamanho_lote: int
) -> list[int]:
    if quantidade <= 0:
        return _obter_ids(session, Conteudo)

    proximo_id_externo = (
        session.scalar(select(func.max(Conteudo.id_externo))) or 0
    ) + 1
    lote: list[object] = []
    inicio = time.perf_counter()
    for indice in range(quantidade):
        tipo = random.choice(TIPOS_CONTEUDO)
        conteudo = Conteudo(
            id_externo=proximo_id_externo + indice,
            api_fonte=(ApiFonte.KITSU if tipo is TipoConteudo.ANIME else ApiFonte.TMDB),
            tipo=tipo,
        )
        lote.extend((conteudo, _criar_detalhe_conteudo(conteudo)))
        if (indice + 1) % tamanho_lote == 0 or indice == quantidade - 1:
            _salvar_lote(session, lote)
            lote = []
            _imprimir_progresso("Conteúdos", indice + 1, quantidade, inicio)
    return _obter_ids(session, Conteudo)


def _pares_disponiveis(
    session: Session,
    modelo: type[ModelT],
    usuario_ids: list[int],
    conteudo_ids: list[int],
    quantidade: int,
) -> list[tuple[int, int]]:
    existentes = set(
        session.execute(
            select(modelo.usuario_id, modelo.conteudo_id)  # type: ignore[attr-defined]
        ).all()
    )
    capacidade = len(usuario_ids) * len(conteudo_ids) - len(existentes)
    if quantidade > capacidade:
        raise ValueError(
            f"Não há combinações suficientes para criar {quantidade} registros de "
            f"{modelo.__tablename__}; capacidade disponível: {capacidade}."
        )

    pares: list[tuple[int, int]] = []
    tentativas = 0
    limite_tentativas = max(quantidade * 20, 100)
    while len(pares) < quantidade and tentativas < limite_tentativas:
        par = (random.choice(usuario_ids), random.choice(conteudo_ids))
        if par not in existentes:
            existentes.add(par)
            pares.append(par)
        tentativas += 1

    if len(pares) < quantidade:
        for usuario_id in usuario_ids:
            for conteudo_id in conteudo_ids:
                par = (usuario_id, conteudo_id)
                if par not in existentes:
                    existentes.add(par)
                    pares.append(par)
                    if len(pares) == quantidade:
                        return pares
    return pares


def _popular_relacao(
    session: Session,
    modelo: type[ModelT],
    quantidade: int,
    tamanho_lote: int,
    rotulo: str,
) -> list[int]:
    usuario_ids = _obter_ids(session, Usuario)
    conteudo_ids = _obter_ids(session, Conteudo)
    if quantidade <= 0:
        return _obter_ids(session, modelo)
    if not usuario_ids or not conteudo_ids:
        raise ValueError(
            f"É necessário possuir usuários e conteúdos antes de criar {rotulo.lower()}."
        )

    pares = _pares_disponiveis(session, modelo, usuario_ids, conteudo_ids, quantidade)
    lote: list[object] = []
    inicio = time.perf_counter()
    for indice, (usuario_id, conteudo_id) in enumerate(pares, start=1):
        lote.append(modelo(usuario_id=usuario_id, conteudo_id=conteudo_id))  # type: ignore[call-arg]
        if indice % tamanho_lote == 0 or indice == quantidade:
            _salvar_lote(session, lote)
            lote = []
            _imprimir_progresso(rotulo, indice, quantidade, inicio)
    return _obter_ids(session, modelo)


def popular_avaliacoes(
    session: Session, quantidade: int, tamanho_lote: int
) -> list[int]:
    usuario_ids = _obter_ids(session, Usuario)
    conteudo_ids = _obter_ids(session, Conteudo)
    if quantidade <= 0:
        return _obter_ids(session, Avaliacao)
    if not usuario_ids or not conteudo_ids:
        raise ValueError(
            "É necessário possuir usuários e conteúdos antes de criar avaliações."
        )

    pares = _pares_disponiveis(
        session, Avaliacao, usuario_ids, conteudo_ids, quantidade
    )
    lote: list[Avaliacao] = []
    inicio = time.perf_counter()
    for indice, (usuario_id, conteudo_id) in enumerate(pares, start=1):
        lote.append(
            Avaliacao(
                usuario_id=usuario_id,
                conteudo_id=conteudo_id,
                estrelas=random.choice(VALORES_ESTRELAS),
                comentario=(
                    fake.sentence(nb_words=random.randint(8, 16))
                    if random.random() < 0.7
                    else None
                ),
            )
        )
        if indice % tamanho_lote == 0 or indice == quantidade:
            _salvar_lote(session, lote)
            lote = []
            _imprimir_progresso("Avaliações", indice, quantidade, inicio)
    return _obter_ids(session, Avaliacao)


def popular_favoritos(
    session: Session, quantidade: int, tamanho_lote: int
) -> list[int]:
    return _popular_relacao(session, Favorito, quantidade, tamanho_lote, "Favoritos")


def popular_assistidos(
    session: Session, quantidade: int, tamanho_lote: int
) -> list[int]:
    return _popular_relacao(session, Assistido, quantidade, tamanho_lote, "Assistidos")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--usuarios", type=int, default=1000)
    parser.add_argument("--conteudos", type=int, default=2000)
    parser.add_argument("--avaliacoes", type=int, default=5000)
    parser.add_argument("--favoritos", type=int, default=3000)
    parser.add_argument("--assistidos", type=int, default=3000)
    parser.add_argument("--batch", type=int, default=1000)
    parser.add_argument("--seed", type=int, help="Seed do gerador aleatório")
    parser.add_argument(
        "--reset", action="store_true", help="Apaga os dados antes de popular o banco"
    )
    args = parser.parse_args()

    quantidades = (
        args.usuarios,
        args.conteudos,
        args.avaliacoes,
        args.favoritos,
        args.assistidos,
    )
    if args.batch <= 0 or any(quantidade < 0 for quantidade in quantidades):
        parser.error("batch deve ser positivo e as quantidades não podem ser negativas")
    if args.seed is not None:
        random.seed(args.seed)
        Faker.seed(args.seed)

    with SessionFactory() as session:
        if args.reset:
            print("Limpando dados existentes...")
            _limpar_banco(session)
        popular_usuarios(session, args.usuarios, args.batch)
        popular_conteudos(session, args.conteudos, args.batch)
        popular_avaliacoes(session, args.avaliacoes, args.batch)
        popular_favoritos(session, args.favoritos, args.batch)
        popular_assistidos(session, args.assistidos, args.batch)

    print("Seed concluído com sucesso.")


if __name__ == "__main__":
    main()
