from enum import Enum
from typing import TypeVar, Generic
from pydantic import BaseModel, Field

T = TypeVar("T")


class OrdenacaoCursor(str, Enum):
    RECENTES = "recentes"
    ANTIGOS = "antigos"


class CursorPaginationParams(BaseModel):
    limit: int = Field(default=20, gt=0, le=20)
    cursor: int = Field(default=0, ge=0)


class CursorMediaPaginationParams(CursorPaginationParams):
    ordenacao: OrdenacaoCursor = OrdenacaoCursor.RECENTES


class CursorPagination(BaseModel):
    cursor: int | None = None
    has_more: bool


class CursorPage(BaseModel, Generic[T]):
    data: list[T]
    pagination: CursorPagination
