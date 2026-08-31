import requests
from typing import Optional
from datetime import datetime, timezone
from requests.exceptions import (
    ConnectionError,
    Timeout,
    TooManyRedirects,
    HTTPError,
    RequestException,
)

from exceptions import ExternalAPIException


def get_now_datetime_utc():
    """
    Retorna no formato UTC (Tempo Universal Coordenado), o datetime do momento
    em que a função for executada.

    OBS: Necessário converter para o horário do usuário no FrontEnd.
    """
    return datetime.now(timezone.utc)


def get_data(url: str, params: Optional[dict] = None, headers: Optional[dict] = None) -> dict:
    """
    Realiza uma requisição GET para uma API externa e retorna o JSON.

    Lança ExternalAPIException em vez de retornar None, permitindo que as rotas
    propaguem o erro com contexto adequado.

    Raises:
        ExternalAPIException: em qualquer falha de rede, timeout ou resposta HTTP
                          com status de erro (4xx / 5xx).
    """
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()

    except Timeout:
        raise ExternalAPIException(
            f"A API externa demorou demais para responder: {url}",
            status_code=504,
        )
    except ConnectionError:
        raise ExternalAPIException(
            f"Não foi possível conectar à API externa: {url}",
            status_code=502,
        )
    except TooManyRedirects:
        raise ExternalAPIException(
            f"Muitos redirecionamentos ao acessar a API externa: {url}",
            status_code=502,
        )
    except HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else 0
        if status == 401:
            raise ExternalAPIException(
                "Chave de API inválida ou sem permissão de acesso.",
                status_code=502,
            )
        if status == 404:
            raise ExternalAPIException(
                "Recurso não encontrado na API externa.",
                status_code=404,
            )
        if status == 429:
            raise ExternalAPIException(
                "Limite de requisições da API externa atingido. Tente novamente mais tarde.",
                status_code=429,
            )
        if status >= 500:
            raise ExternalAPIException(
                f"A API externa retornou um erro interno (HTTP {status}).",
                status_code=502,
            )
        raise ExternalAPIException(
            f"Erro HTTP {status} ao acessar a API externa.",
            status_code=502,
        )
    except RequestException as exc:
        raise ExternalAPIException(
            f"Erro inesperado ao acessar a API externa: {exc}",
            status_code=502,
        )
