from typing import Any

from beanie import PydanticObjectId
from pydantic import BaseModel


class BaseResponse(BaseModel):
    success: bool = True
    detail: Any = None


class ListResponse(BaseResponse):
    total_count: int = 0
    detail: list[Any] = []


class Login(BaseModel):
    tckn: int
    password: str


class Filter(BaseModel):
    page_size: int = 10
    page: int = 0
    keyword: str = ""
    sort: str = "_id"


class NameId(BaseModel):
    name: str | None = None
    id_: PydanticObjectId = None
