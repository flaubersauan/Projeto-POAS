from typing import Annotated

from fastapi import Depends

from exceptions import ConflictException, NotFoundException
from models import Avaliacao
from repositories import AvaliacaoRepositoryDep
from schemas.avaliacao import AvaliacaoCreate, AvaliacaoUpdate, AvaliacaoSerieRead, AvaliacaoFilmeRead, AvaliacaoAnimeRead
from services.usuario import UsuarioServiceDep
from services.conteudo import ConteudoServiceDep
from services.serie import SerieServiceDep
from services.filme import FilmeServiceDep
from services.anime import AnimeServiceDep


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

    def list_avaliacoes_usuario(self, usuario_id: int) -> list[Avaliacao]:
        """Retorna as avaliações do usuário autenticado."""
        usuario = self.usuario_service.get_usuario(usuario_id)
        return self.avaliacao_repository.list_avaliacoes_by_usuario(usuario)

    def list_avaliacoes_conteudo(self, serie_id: int) -> list[Avaliacao]:
        """Retorna todas as avaliações de uma série específica."""
        serie = self.serie_service.get_serie_from_db(serie_id)
        if not serie:
            _, serie = self.serie_service.get_serie_from_api_and_update_database(serie_id)
        avaliacoes = self.avaliacao_repository.list_avaliacoes_by_conteudo(
            serie.conteudo
        )

        return [
            AvaliacaoSerieRead(
                id=a.id,
                usuario_id=a.usuario_id,
                estrelas=a.estrelas,
                comentario=a.comentario,
                data_criacao=a.data_criacao,
                data_atualizacao=a.data_atualizacao,
                serie_id=serie_id,
            )
            for a in avaliacoes
        ]

    # --- Filme evaluations ---
    def list_avaliacoes_filme(self, filme_id: int) -> list[Avaliacao]:
        filme = self.filme_service.get_filme_from_db(filme_id)
        if not filme:
            _, filme = self.filme_service.get_filme_from_api_and_update_database(filme_id)

        avaliacoes = self.avaliacao_repository.list_avaliacoes_by_conteudo(
            filme.conteudo
        )

        from schemas.avaliacao import AvaliacaoFilmeRead

        return [
            AvaliacaoFilmeRead(
                id=a.id,
                usuario_id=a.usuario_id,
                estrelas=a.estrelas,
                comentario=a.comentario,
                data_criacao=a.data_criacao,
                data_atualizacao=a.data_atualizacao,
                filme_id=filme_id,
            )
            for a in avaliacoes
        ]

    def create_avaliacao_filme(
        self, filme_id: int, usuario_id: int, avaliacao_data: AvaliacaoCreate
    ) -> Avaliacao:
        usuario = self.usuario_service.get_usuario(usuario_id)
        filme = self.filme_service.get_filme_from_db(filme_id)
        if not filme:
            _, filme = self.filme_service.get_filme_from_api_and_update_database(filme_id)

        avaliacao_existente = self.avaliacao_repository.get_avaliacao_by_usuario_and_conteudo(
            usuario,
            filme.conteudo,
        )
        if avaliacao_existente:
            raise ConflictException("Você já avaliou este filme")

        avaliacao = Avaliacao(
            conteudo=filme.conteudo,
            usuario=usuario,
            estrelas=avaliacao_data.estrelas,
            comentario=avaliacao_data.comentario,
        )

        avaliacao_criada = self.avaliacao_repository.create_avaliacao(avaliacao)

        from schemas.avaliacao import AvaliacaoFilmeRead

        return AvaliacaoFilmeRead(
            id=avaliacao_criada.id,
            usuario_id=avaliacao_criada.usuario_id,
            estrelas=avaliacao_criada.estrelas,
            comentario=avaliacao_criada.comentario,
            data_criacao=avaliacao_criada.data_criacao,
            data_atualizacao=avaliacao_criada.data_atualizacao,
            filme_id=filme_id,
        )

    def update_avaliacao_filme(
        self, filme_id: int, usuario_id: int, avaliacao_data: AvaliacaoUpdate
    ) -> AvaliacaoFilmeRead:
        usuario = self.usuario_service.get_usuario(usuario_id)
        filme = self.filme_service.get_filme_from_db(filme_id)
        if not filme:
            _, filme = self.filme_service.get_filme_from_api_and_update_database(filme_id)

        avaliacao = self.avaliacao_repository.get_avaliacao_by_usuario_and_conteudo(
            usuario,
            filme.conteudo,
        )
        if not avaliacao:
            raise NotFoundException("Avaliação do filme não encontrada para o usuário atual")

        if avaliacao_data.estrelas is not None:
            avaliacao.estrelas = avaliacao_data.estrelas
        if avaliacao_data.comentario is not None:
            avaliacao.comentario = avaliacao_data.comentario

        avaliacao_atualizada = self.avaliacao_repository.update_avaliacao(avaliacao)

        from schemas.avaliacao import AvaliacaoFilmeRead

        return AvaliacaoFilmeRead(
            id=avaliacao_atualizada.id,
            usuario_id=avaliacao_atualizada.usuario_id,
            estrelas=avaliacao_atualizada.estrelas,
            comentario=avaliacao_atualizada.comentario,
            data_criacao=avaliacao_atualizada.data_criacao,
            data_atualizacao=avaliacao_atualizada.data_atualizacao,
            filme_id=filme_id,
        )

    def delete_avaliacao_filme(self, filme_id: int, usuario_id: int):
        usuario = self.usuario_service.get_usuario(usuario_id)
        filme = self.filme_service.get_filme_from_db(filme_id)
        if not filme:
            _, filme = self.filme_service.get_filme_from_api_and_update_database(filme_id)

        avaliacao = self.avaliacao_repository.get_avaliacao_by_usuario_and_conteudo(
            usuario,
            filme.conteudo,
        )
        if not avaliacao:
            raise NotFoundException("Avaliação do filme não encontrada para o usuário atual")

        self.avaliacao_repository.delete_avaliacao(avaliacao)

    # --- Anime evaluations ---
    def list_avaliacoes_anime(self, anime_id: int) -> list[Avaliacao]:
        anime = self.anime_service.get_anime_from_db(anime_id)
        if not anime:
            _, anime = self.anime_service.get_anime_from_api_and_update_database(anime_id)

        avaliacoes = self.avaliacao_repository.list_avaliacoes_by_conteudo(
            anime.conteudo
        )

        from schemas.avaliacao import AvaliacaoAnimeRead

        return [
            AvaliacaoAnimeRead(
                id=a.id,
                usuario_id=a.usuario_id,
                estrelas=a.estrelas,
                comentario=a.comentario,
                data_criacao=a.data_criacao,
                data_atualizacao=a.data_atualizacao,
                anime_id=anime_id,
            )
            for a in avaliacoes
        ]

    def create_avaliacao_anime(
        self, anime_id: int, usuario_id: int, avaliacao_data: AvaliacaoCreate
    ) -> Avaliacao:
        usuario = self.usuario_service.get_usuario(usuario_id)
        anime = self.anime_service.get_anime_from_db(anime_id)
        if not anime:
            _, anime = self.anime_service.get_anime_from_api_and_update_database(anime_id)

        avaliacao_existente = self.avaliacao_repository.get_avaliacao_by_usuario_and_conteudo(
            usuario,
            anime.conteudo,
        )
        if avaliacao_existente:
            raise ConflictException("Você já avaliou este anime")

        avaliacao = Avaliacao(
            conteudo=anime.conteudo,
            usuario=usuario,
            estrelas=avaliacao_data.estrelas,
            comentario=avaliacao_data.comentario,
        )

        avaliacao_criada = self.avaliacao_repository.create_avaliacao(avaliacao)

        from schemas.avaliacao import AvaliacaoAnimeRead

        return AvaliacaoAnimeRead(
            id=avaliacao_criada.id,
            usuario_id=avaliacao_criada.usuario_id,
            estrelas=avaliacao_criada.estrelas,
            comentario=avaliacao_criada.comentario,
            data_criacao=avaliacao_criada.data_criacao,
            data_atualizacao=avaliacao_criada.data_atualizacao,
            anime_id=anime_id,
        )

    def update_avaliacao_anime(
        self, anime_id: int, usuario_id: int, avaliacao_data: AvaliacaoUpdate
    ) -> AvaliacaoAnimeRead:
        usuario = self.usuario_service.get_usuario(usuario_id)
        anime = self.anime_service.get_anime_from_db(anime_id)
        if not anime:
            _, anime = self.anime_service.get_anime_from_api_and_update_database(anime_id)

        avaliacao = self.avaliacao_repository.get_avaliacao_by_usuario_and_conteudo(
            usuario,
            anime.conteudo,
        )
        if not avaliacao:
            raise NotFoundException("Avaliação do anime não encontrada para o usuário atual")

        if avaliacao_data.estrelas is not None:
            avaliacao.estrelas = avaliacao_data.estrelas
        if avaliacao_data.comentario is not None:
            avaliacao.comentario = avaliacao_data.comentario

        avaliacao_atualizada = self.avaliacao_repository.update_avaliacao(avaliacao)

        from schemas.avaliacao import AvaliacaoAnimeRead

        return AvaliacaoAnimeRead(
            id=avaliacao_atualizada.id,
            usuario_id=avaliacao_atualizada.usuario_id,
            estrelas=avaliacao_atualizada.estrelas,
            comentario=avaliacao_atualizada.comentario,
            data_criacao=avaliacao_atualizada.data_criacao,
            data_atualizacao=avaliacao_atualizada.data_atualizacao,
            anime_id=anime_id,
        )

    def delete_avaliacao_anime(self, anime_id: int, usuario_id: int):
        usuario = self.usuario_service.get_usuario(usuario_id)
        anime = self.anime_service.get_anime_from_db(anime_id)
        if not anime:
            _, anime = self.anime_service.get_anime_from_api_and_update_database(anime_id)

        avaliacao = self.avaliacao_repository.get_avaliacao_by_usuario_and_conteudo(
            usuario,
            anime.conteudo,
        )
        if not avaliacao:
            raise NotFoundException("Avaliação do anime não encontrada para o usuário atual")

        self.avaliacao_repository.delete_avaliacao(avaliacao)

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

        avaliacao_criada = self.avaliacao_repository.create_avaliacao(avaliacao)

        return AvaliacaoSerieRead(
            id=avaliacao_criada.id,
            usuario_id=avaliacao_criada.usuario_id,
            estrelas=avaliacao_criada.estrelas,
            comentario=avaliacao_criada.comentario,
            data_criacao=avaliacao_criada.data_criacao,
            data_atualizacao=avaliacao_criada.data_atualizacao,
            serie_id=serie_id,
        )

    def update_avaliacao(
        self, serie_id: int, usuario_id: int, avaliacao_data: AvaliacaoUpdate
    ) -> AvaliacaoSerieRead:
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

        avaliacao_atualizada = self.avaliacao_repository.update_avaliacao(avaliacao)

        return AvaliacaoSerieRead(
            id=avaliacao_atualizada.id,
            usuario_id=avaliacao_atualizada.usuario_id,
            estrelas=avaliacao_atualizada.estrelas,
            comentario=avaliacao_atualizada.comentario,
            data_criacao=avaliacao_atualizada.data_criacao,
            data_atualizacao=avaliacao_atualizada.data_atualizacao,
            serie_id=serie_id,
        )

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
