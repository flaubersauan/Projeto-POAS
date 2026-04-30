# from sqlalchemy import URL
from sqlmodel import Session, SQLModel, create_engine
from fastapi import Depends
from typing import Annotated

# DB_URL = URL.create(
#     drivername="sqlite",
#     username="moviescore",
#     password="",
#     host="localhost",
#     database="moviescore"
# )

DB_URL = "sqlite:///database.db"
ARGS = {"check_same_thread":False}

engine = create_engine(DB_URL, connect_args=ARGS)


def create_db():
    from models import (
        Usuario,   
    )

    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
