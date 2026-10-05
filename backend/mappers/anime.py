from schemas.anime import AnimeRead, CategoriaRead, ImagensAnime, StatusAnime

class AnimeMapper:
    STATUS_MAP = {
        "current": StatusAnime.ANDAMENTO,
        "finished": StatusAnime.FINALIZADO,
        "tba": StatusAnime.A_SER_ANUNCIADO,
        "unreleased": StatusAnime.NAO_LANCADO,
        "upcoming": StatusAnime.POR_VIR,
    }

    # Mapa reverso (StatusAnime -> valor do filter[status] do Kitsu)
    STATUS_TO_KITSU = {status: kitsu for kitsu, status in STATUS_MAP.items()}

    @staticmethod
    def map_status(status: str | None) -> StatusAnime:
        if status not in AnimeMapper.STATUS_MAP:
            print(f"Status desconhecido recebido do Kitsu: {status}")

        return AnimeMapper.STATUS_MAP.get(status, StatusAnime.DESCONHECIDO)

    @staticmethod
    def _map_localized(value) -> str:
        """Campos como title/description do Kitsu podem vir como string ou dict por idioma."""
        if isinstance(value, dict):
            return value.get("pt-BR") or value.get("pt-br") or value.get("en") or ""

        return value or ""

    @staticmethod
    def _map_genres(item: dict, included: list[dict]) -> list[dict]:
        relationships = item.get("relationships", {})
        genre_data = relationships.get("genres", {}).get("data", [])

        included_by_id = {
            resource["id"]: resource
            for resource in included
            if resource.get("type") == "genres"
        }

        return [
            {
                "id": int(genre["id"]),
                "nome": included_by_id[genre["id"]]["attributes"]["name"],
            }
            for genre in genre_data
            if genre["id"] in included_by_id
        ]

    @staticmethod
    def _map_categories(item: dict, included: list[dict]) -> list[dict]:
        relationships = item.get("relationships", {})
        category_data = relationships.get("categories", {}).get("data", [])

        included_by_id = {
            resource["id"]: resource
            for resource in included
            if resource.get("type") == "categories"
        }

        return [
            {
                "id": int(category["id"]),
                "nome": AnimeMapper._map_localized(
                    included_by_id[category["id"]].get("attributes", {}).get("title")
                ),
            }
            for category in category_data
            if category["id"] in included_by_id
        ]

    @staticmethod
    def map_anime(item: dict, included: list[dict]) -> AnimeRead:
        attributes: dict = item["attributes"]

        poster_image = attributes.get("posterImage") or {}
        cover_image = attributes.get("coverImage") or {}

        return AnimeRead(
            id=int(item["id"]),
            titulos=attributes.get("titles") or {},
            titulo_canonico=attributes.get("canonicalTitle") or "",
            descricao=attributes.get("description"),
            status=AnimeMapper.map_status(attributes.get("status")),
            data_inicio=attributes.get("startDate"),
            data_fim=attributes.get("endDate"),
            quantidade_episodios=attributes.get("episodeCount"),
            duracao_episodios=attributes.get("episodeLength"),
            imagens=ImagensAnime(
                capa=poster_image.get("original"),
                banner=cover_image.get("original"),
            ),
            generos=AnimeMapper._map_genres(item, included),
            categorias=AnimeMapper._map_categories(item, included),
        )

    @staticmethod
    def map_animes(items: list[dict], included: list[dict]) -> list[AnimeRead]:
        return [
            AnimeMapper.map_anime(item, included)
            for item in items
        ]

    @staticmethod
    def map_categoria(item: dict) -> CategoriaRead:
        attributes: dict = item.get("attributes", {})

        return CategoriaRead(
            id=int(item["id"]),
            nome=AnimeMapper._map_localized(attributes.get("title")),
            slug=attributes.get("slug") or "",
            descricao=AnimeMapper._map_localized(attributes.get("description")) or None,
            total_midias=attributes.get("totalMediaCount"),
        )

    @staticmethod
    def map_categorias(items: list[dict]) -> list[CategoriaRead]:
        return [
            AnimeMapper.map_categoria(item)
            for item in items
        ]
