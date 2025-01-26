from typing import List

from pydantic import BaseModel


class FibonacciResponse(BaseModel):
    number: int
    fibonacci: int


class FibonacciListResponse(BaseModel):
    page: int
    page_size: int
    numbers: List[FibonacciResponse]


class BlacklistRequest(BaseModel):
    number: int


class BlacklistResponse(BaseModel):
    message: str
