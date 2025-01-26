from pydantic import BaseModel


class FibonacciResponse(BaseModel):
    number: int
    fibonacci: int
