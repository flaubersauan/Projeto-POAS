from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from os import getenv
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY não encontrada no arquivo .env")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("JWT_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(getenv("JWT_REFRESH_EXPIRE_DAYS", 7))


def _create_token(data: dict, token_type: str, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    to_encode.update(
        {
            "exp": datetime.now(timezone.utc) + expires_delta,
            "type": token_type,
        }
    )
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Gera um JWT de acesso com os dados fornecidos."""
    return _create_token(
        data,
        "access",
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def create_refresh_token(data: dict) -> str:
    """Gera um JWT de renovação com validade maior que a do token de acesso."""
    return _create_token(
        data,
        "refresh",
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )


def _decode_token(token: str, expected_type: str) -> dict:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    if payload.get("type") != expected_type:
        raise JWTError("Tipo de token inválido")
    return payload


def decode_access_token(token: str) -> dict:
    """Decodifica e valida um JWT de acesso."""
    return _decode_token(token, "access")


def decode_refresh_token(token: str) -> dict:
    """Decodifica e valida um JWT de renovação."""
    return _decode_token(token, "refresh")
