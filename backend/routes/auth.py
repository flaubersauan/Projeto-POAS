from fastapi import APIRouter

from schemas.auth import LoginInput, RefreshTokenInput, TokenResponse
from schemas.usuario import UsuarioRead
from services import AuthServiceDep
from auth import CurrentUsuarioDep

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login", response_model=TokenResponse)
def login(dados: LoginInput, auth_service: AuthServiceDep):
    """
    Autentica o usuário com email e senha.
    Retorna um JWT de acesso em caso de sucesso.
    """
    access_token, refresh_token = auth_service.autenticar(dados)
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@auth_router.post("/refresh", response_model=TokenResponse)
def refresh(dados: RefreshTokenInput, auth_service: AuthServiceDep):
    """Emite um novo par de tokens a partir de um refresh token válido."""
    access_token, refresh_token = auth_service.renovar_tokens(dados.refresh_token)
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@auth_router.get("/me", response_model=UsuarioRead)
def me(usuario_atual: CurrentUsuarioDep):
    """Retorna os dados do usuário autenticado."""
    return usuario_atual
