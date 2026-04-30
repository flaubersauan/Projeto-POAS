from fastapi import FastAPI
from contextlib import asynccontextmanager

from routes import animes_router, filmes_router, usuario_router
from utils import gerar_env
from database import create_db


gerar_env()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(usuario_router)
app.include_router(animes_router)
app.include_router(filmes_router)