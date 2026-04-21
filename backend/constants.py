from dotenv import load_dotenv
from os import getenv

load_dotenv()

KITSU_API_URL = "https://kitsu.io/api/edge"
TMDB_API_URL = "https://api.themoviedb.org/3"

TMDB_KEY = getenv("TMBD_API_KEY")

PARAMS_TMDB = {
    "language": "pt-BR"
}
HEADERS_TMDB = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_KEY}"
}