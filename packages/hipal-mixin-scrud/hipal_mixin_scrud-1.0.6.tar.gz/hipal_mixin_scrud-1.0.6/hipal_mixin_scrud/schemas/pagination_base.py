from pydantic import BaseModel
from typing import Dict, List


class Links(BaseModel):
    first: str
    prev: str
    next: str
    last: str


class Pagination(BaseModel):
    offset: int
    limit: int
    total: int
    total_pages: int
    links: Links


class PaginationBase(BaseModel):
    data: List[Dict]
    pagination: Pagination
