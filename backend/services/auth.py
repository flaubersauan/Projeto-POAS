from typing import Annotated

from fastapi import Depends, HTTPException, status

from jose import JWTError

from auth import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    verify_password,
)
from repositories import UsuarioRepositoryDep
from schemas.auth import LoginInput


class AuthService:
    def __init__(self, usuario_repository: UsuarioRepositoryDep):
        self.usuario_repository = usuario_repository

    def autenticar(self, dados: LoginInput) -> tuple[str, str]:
        usuario = self.usuario_repository.get_usuario_by_email(dados.email)

        if not usuario or not verify_password(dados.senha, usuario.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return self._criar_par_de_tokens(usuario.id)

    def renovar_tokens(self, refresh_token: str) -> tuple[str, str]:
        try:
            payload = decode_refresh_token(refresh_token)
            usuario_id = int(payload["sub"])
        except (JWTError, KeyError, TypeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token inválido ou expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )

        usuario = self.usuario_repository.get_usuario(usuario_id)
        if usuario is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token inválido ou expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return self._criar_par_de_tokens(usuario.id)

    @staticmethod
    def _criar_par_de_tokens(usuario_id: int) -> tuple[str, str]:
        dados = {"sub": str(usuario_id)}
        return create_access_token(data=dados), create_refresh_token(data=dados)


AuthServiceDep = Annotated[AuthService, Depends(AuthService)]
