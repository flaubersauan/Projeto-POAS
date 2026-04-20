from fastapi import FastAPI
import requests

def get_data(url, params):
    request = requests.get(url, params)

    try:
        data = request.json()
    except Exception as e:
        print(e)

    return data

KITSU_API_URL = "https://kitsu.io/api/edge"

app = FastAPI()

@app.get("/anime")
def listar_animes(title: str | None = None):
    url = KITSU_API_URL+"/anime"
    params = {}
    
    if title:
        params["filter[text]"] = title

    animes = get_data(url, params)
    return animes