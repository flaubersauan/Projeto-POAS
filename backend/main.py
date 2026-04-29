from fastapi import FastAPI
from contextlib import asynccontextmanager

from routes import animes_router, filmes_router
from utils import gerar_env


gerar_env()

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    #create_db()
    yield

app.include_router(animes_router)
app.include_router(filmes_router)