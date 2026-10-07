from pathlib import Path
from dotenv import load_dotenv
from os import getenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env", encoding="utf-8-sig")


def _get_env(name: str) -> str:
    value = getenv(name)
    if value is None:
        return ""
    return value.strip().strip('"').strip("'")


STORAGE = "storage/usuarios/fotos"
BASE_URL = _get_env("BASE_URL")  # utilizada no retorno da foto_perfil_url do usuário
if not BASE_URL:
    raise ValueError("BASE_URL não encontrado no arquivo .env")

KITSU_API_URL = "https://kitsu.io/api/edge"
TMDB_API_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_STORAGE = "https://image.tmdb.org/t/p"

TMDB_KEY = _get_env("TMDB_API_KEY")
if not TMDB_KEY:
    raise ValueError("TMDB_API_KEY não encontrada no arquivo .env")

PARAMS_TMDB = {
    "language": "pt-BR"
}

HEADERS_TMDB = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_KEY}"
}
HEADERS_KITSU = {
    "Accept": "application/vnd.api+json",
    "Content-Type": "application/vnd.api+json",
}
