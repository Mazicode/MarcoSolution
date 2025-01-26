from fastapi import APIRouter, HTTPException

from app.docs import FIBONACCI_DOCS, FIBONACCI_LIST_DOCS, BLACKLIST_ADD_DOCS, BLACKLIST_REMOVE_DOCS
from app.schemas import FibonacciResponse, FibonacciListResponse, BlacklistRequest
from app.utils import fibonacci, paginate

router = APIRouter()

# In-memory storage for caching blacklisted numbers and Fibonacci numbers
blacklist = set()
fibonacci_cache = {}


def get_blacklist():
    return blacklist


@router.get("/fibonacci/{number}", response_model=FibonacciResponse, **FIBONACCI_DOCS)
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


@router.get("/fibonacci", response_model=FibonacciListResponse, **FIBONACCI_LIST_DOCS)
def get_fibonacci_list(
        n: int,
        page: int = 1,
        page_size: int = 100,
):
    blacklist = get_blacklist()

    if n <= 0:
        raise HTTPException(status_code=422, detail="The 'n' parameter must be a positive integer.")
    if page <= 0 or page_size <= 0:
        raise HTTPException(status_code=422, detail="Page and page size must be positive integers.")

    result = paginate(n, page, page_size, blacklist)

    for item in result["numbers"]:
        number = item["number"]
        if number in fibonacci_cache:
            item["fibonacci"] = fibonacci_cache[number]
        else:
            item["fibonacci"] = fibonacci(number)
            fibonacci_cache[number] = item["fibonacci"]  # Cache the result

    return result


@router.post("/blacklist", **BLACKLIST_ADD_DOCS)
def blacklist_number(request: BlacklistRequest):
    if request.number <= 0:
        raise HTTPException(status_code=422, detail="Only positive integers can be blacklisted.")
    blacklist.add(request.number)
    return {"message": f"Number {request.number} has been blacklisted."}


@router.delete("/blacklist", **BLACKLIST_REMOVE_DOCS)
def remove_from_blacklist(request: BlacklistRequest):
    blacklist.discard(request.number)  # Safely remove without error if not present
    return {"message": f"Number {request.number} has been removed from the blacklist."}


@router.get("/health")
def health_check():
    return {"status": "healthy"}
