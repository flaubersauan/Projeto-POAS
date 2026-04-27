from fastapi import APIRouter
from constants import TMDB_API_URL, HEADERS_TMDB, PARAMS_TMDB
from utils import get_data

filmes_router = APIRouter(prefix="/filme", tags=["filme"])

@filmes_router.get("")
def buscar_filmes(busca: str):
    url = TMDB_API_URL+"/search/movie"
    params = PARAMS_TMDB.copy()

    if busca:
        params["query"] = busca

    filmes = get_data(url, params, HEADERS_TMDB)
    return filmes

@filmes_router.get("/em-alta")
def listar_filmes_em_alta():
    url = TMDB_API_URL+"/trending/movie/week"

    filmes = get_data(url, PARAMS_TMDB, HEADERS_TMDB)
    return filmes