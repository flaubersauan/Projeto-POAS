from fastapi import FastAPI
from routes import animes_router, filmes_router
from utils import gerar_env

gerar_env()

app = FastAPI()

app.include_router(animes_router)
app.include_router(filmes_router)