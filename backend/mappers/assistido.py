from schemas.conteudo import ImagensConteudo
from schemas.assistido import AnimeAssistidoRead, FilmeAssistidoRead, SerieAssistidaRead
from models import Anime, Assistido, Filme, Serie
from .filme import FilmeMapper
from .serie import SerieMapper


class AssistidoMapper:
    @staticmethod
    def map_serie(serie: Serie, assistido: Assistido) -> SerieAssistidaRead:
        return SerieAssistidaRead(
            id=serie.conteudo.id_externo,
            titulo=serie.titulo,
            titulo_original=serie.titulo_original,
            status=serie.status,
            imagens=ImagensConteudo(
                capa=SerieMapper.map_image(serie.capa, "w500"),
                banner=SerieMapper.map_image(serie.banner, "original"),
            ),
            data_lancamento=serie.data_lancamento,
            data_adicao=assistido.data_adicao,
        )

    @staticmethod
    def map_series(items: list[tuple[Serie, Assistido]]) -> list[SerieAssistidaRead]:
        return [
            AssistidoMapper.map_serie(serie, assistido)
            for serie, assistido in items
        ]

    @staticmethod
    def map_filme(filme: Filme, assistido: Assistido) -> FilmeAssistidoRead:
        return FilmeAssistidoRead(
            id=filme.conteudo.id_externo,
            titulo=filme.titulo,
            titulo_original=filme.titulo_original,
            status=filme.status,
            imagens=ImagensConteudo(
                capa=FilmeMapper.map_image(filme.capa, "w500"),
                banner=FilmeMapper.map_image(filme.banner, "original"),
            ),
            data_lancamento=filme.data_lancamento,
            data_adicao=assistido.data_adicao,
        )

    @staticmethod
    def map_filmes(items: list[tuple[Filme, Assistido]]) -> list[FilmeAssistidoRead]:
        return [
            AssistidoMapper.map_filme(filme, assistido)
            for filme, assistido in items
        ]

    @staticmethod
    def map_anime(anime: Anime, assistido: Assistido) -> AnimeAssistidoRead:
        # Kitsu já retorna URLs completas, sem prefixo de imagem do TMDB
        return AnimeAssistidoRead(
            id=anime.conteudo.id_externo,
            titulo=anime.titulo,
            titulo_original=anime.titulo_original,
            status=anime.status,
            imagens=ImagensConteudo(
                capa=anime.capa,
                banner=anime.banner,
            ),
            data_lancamento=anime.data_lancamento,
            data_adicao=assistido.data_adicao,
        )

    @staticmethod
    def map_animes(items: list[tuple[Anime, Assistido]]) -> list[AnimeAssistidoRead]:
        return [
            AssistidoMapper.map_anime(anime, assistido)
            for anime, assistido in items
        ]
