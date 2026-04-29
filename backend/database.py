from sqlalchemy import URL
from sqlmodel import Session
from fastapi import Depends
from typing import Annotated

ENGINE = URL.create(
    drivername="sqlite",
    username="moviescore",
    password="",
    host="localhost",
    database="moviescore"
)

def get_session():
    with Session(ENGINE) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
