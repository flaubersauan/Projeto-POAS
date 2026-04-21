from fastapi import APIRouter
from constants import KITSU_API_URL
from utils import get_data

animes_router = APIRouter(prefix="/anime", tags=["anime"])

@animes_router.get("")
def buscar_animes(busca: str):
    url = KITSU_API_URL+"/anime"
    params = {}
    
    if busca:
        params["filter[text]"] = busca

    animes = get_data(url, params)
    return animes