from fastapi import APIRouter, HTTPException, Depends
from redis.client import Redis
from app.redis import get_redis_connection
from app.utils import fibonacci, paginate, get_blacklist
from app.schemas import FibonacciResponse, FibonacciListResponse, BlacklistRequest
from app.docs import FIBONACCI_DOCS, FIBONACCI_LIST_DOCS, BLACKLIST_ADD_DOCS, BLACKLIST_REMOVE_DOCS
from app.exceptions import InvalidNumberError, PaginationError

router = APIRouter()


@router.get("/fibonacci/{number}", response_model=FibonacciResponse, **FIBONACCI_DOCS)
def get_fibonacci_number(number: int, redis_conn: Redis = Depends(get_redis_connection)):
    blacklist = get_blacklist(redis_conn)
    if number in blacklist:
        raise HTTPException(status_code=400, detail="Number is blacklisted.")

    try:
        fib_result = fibonacci(number)
        return {"number": number, "fibonacci": fib_result}
    except InvalidNumberError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("/fibonacci", response_model=FibonacciListResponse, **FIBONACCI_LIST_DOCS)
def get_fibonacci_list(
        n: int,
        page: int = 1,
        page_size: int = 100,
        redis_conn: Redis = Depends(get_redis_connection),
):
    blacklist = get_blacklist(redis_conn)

    try:
        result = paginate(n, page, page_size, blacklist)
    except PaginationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    for item in result["numbers"]:
        item["fibonacci"] = fibonacci(item["number"])

    return result


@router.post("/blacklist", **BLACKLIST_ADD_DOCS)
def blacklist_number(
        request: BlacklistRequest, redis_conn: Redis = Depends(get_redis_connection)
):
    redis_conn.sadd("blacklist", request.number)
    return {"message": f"Number {request.number} has been blacklisted."}


@router.delete("/blacklist", **BLACKLIST_REMOVE_DOCS)
def remove_from_blacklist(
        request: BlacklistRequest, redis_conn: Redis = Depends(get_redis_connection)
):
    redis_conn.srem("blacklist", request.number)
    return {"message": f"Number {request.number} has been removed from the blacklist."}


@router.get("/health")
def health_check():
    return {"status": "healthy"}
