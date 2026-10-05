from schemas.conteudo import ImagensConteudo
from schemas.favorito import AnimeFavoritoRead, FilmeFavoritoRead, SerieFavoritaRead
from models import (
    Anime,
    Favorito,
    Filme,
    Serie,
)
from .filme import FilmeMapper
from .serie import SerieMapper


class FavoritoMapper:
    @staticmethod
    def map_serie(serie: Serie, favorito: Favorito) -> SerieFavoritaRead:
        return SerieFavoritaRead(
            id=serie.conteudo.id_externo,
            titulo=serie.titulo,
            titulo_original=serie.titulo_original,
            status=serie.status,
            imagens=ImagensConteudo(
                capa=SerieMapper.map_image(serie.capa, "w500"),
                banner=SerieMapper.map_image(serie.banner, "original")
            ),
            data_lancamento=serie.data_lancamento,
            data_adicao=favorito.data_adicao
        )

    @staticmethod
    def map_series(items: list[tuple[Serie, Favorito]]) -> list[SerieFavoritaRead]:
        return [
            FavoritoMapper.map_serie(serie, favorito)
            for serie, favorito in items
        ]

    @staticmethod
    def map_filme(filme: Filme, favorito: Favorito) -> FilmeFavoritoRead:
        return FilmeFavoritoRead(
            id=filme.conteudo.id_externo,
            titulo=filme.titulo,
            titulo_original=filme.titulo_original,
            status=filme.status,
            imagens=ImagensConteudo(
                capa=FilmeMapper.map_image(filme.capa, "w500"),
                banner=FilmeMapper.map_image(filme.banner, "original")
            ),
            data_lancamento=filme.data_lancamento,
            data_adicao=favorito.data_adicao,
        )

    @staticmethod
    def map_filmes(items: list[tuple[Filme, Favorito]]) -> list[FilmeFavoritoRead]:
        return [
            FavoritoMapper.map_filme(filme, favorito)
            for filme, favorito in items
        ]

    @staticmethod
    def map_anime(anime: Anime, favorito: Favorito) -> AnimeFavoritoRead:
        # Kitsu já retorna URLs completas, sem prefixo de imagem do TMDB
        return AnimeFavoritoRead(
            id=anime.conteudo.id_externo,
            titulo=anime.titulo,
            titulo_original=anime.titulo_original,
            status=anime.status,
            imagens=ImagensConteudo(
                capa=anime.capa,
                banner=anime.banner,
            ),
            data_lancamento=anime.data_lancamento,
            data_adicao=favorito.data_adicao,
        )

    @staticmethod
    def map_animes(items: list[tuple[Anime, Favorito]]) -> list[AnimeFavoritoRead]:
        return [
            FavoritoMapper.map_anime(anime, favorito)
            for anime, favorito in items
        ]