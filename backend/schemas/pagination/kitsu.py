from typing import TypeVar, Generic
from pydantic import BaseModel, Field

T = TypeVar("T")


class KitsuPaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    # limit: int = Field(default=20, gt=0, le=20)

    def to_kitsu_query_params(self):
        return {"page[number]": self.page, "page[size]": 20}


class KitsuPagination(BaseModel):
    page: int
    # limit: int
    total_results: int
    has_more: bool


class KitsuPage(BaseModel, Generic[T]):
    data: list[T]
    pagination: KitsuPagination
