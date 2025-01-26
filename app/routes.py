from fastapi import APIRouter, HTTPException

from app.schemas import FibonacciResponse
from app.utils import fibonacci

router = APIRouter()

# In-memory storage for caching blacklisted numbers and Fibonacci numbers
blacklist = set()
fibonacci_cache = {}


def get_blacklist():
    return blacklist


@router.get("/fibonacci/{number}", response_model=FibonacciResponse)
def get_fibonacci_number(number: int):
    local_blacklist = get_blacklist()
    if number in local_blacklist:
        raise HTTPException(status_code=400, detail="Number is blacklisted.")

    if number in fibonacci_cache:
        fib_result = fibonacci_cache[number]
    else:
        if number <= 0:
            raise HTTPException(status_code=422, detail="Fibonacci number must be a positive integer.")
        fib_result = fibonacci(number)
        fibonacci_cache[number] = fib_result

    return {"number": number, "fibonacci": fib_result}
