from redis.client import Redis

from app.exceptions import InvalidPageSizeError, InvalidPageNumberError, InvalidTotalItemsError, \
    PageExceedsTotalPagesError, InvalidNumberError


def fibonacci(n: int) -> int:
    """Calculate Fibonacci value for a given number."""
    if n <= 0:
        raise InvalidNumberError(n)
    if n == 1 or n == 2:
        return 1

    a, b = 1, 1
    for _ in range(2, n):
        a, b = b, a + b

    return b


def paginate(n: int, page: int, page_size: int = 10, blacklist: set = None):
    """
    Paginate a list of Fibonacci numbers.

    Parameters:
        n (int): Total number of Fibonacci numbers to calculate.
        page (int): The page number to retrieve.
        page_size (int, optional): Number of items per page. Defaults to 10.
        blacklist (set, optional): Set of numbers to exclude from pagination.

    Returns:
        dict: A dictionary containing the current page, page size, numbers, and total pages.

    Raises:
        ValueError: If page_size, page, or n are not positive integers, or if page exceeds the total number of pages.
    """
    if page_size <= 0:
        raise InvalidPageSizeError(page_size)
    if page <= 0:
        raise InvalidPageNumberError(page)
    if n <= 0:
        raise InvalidTotalItemsError(n)

    blacklist = blacklist or set()

    numbers = [
        {"number": i, "fibonacci": fibonacci(i)}
        for i in range(1, n + 1) if i not in blacklist
    ]
    total_pages = (len(numbers) + page_size - 1) // page_size

    # Gracefully handle the case where there are no numbers available
    if total_pages == 0:
        return {
            "page": page,
            "page_size": page_size,
            "numbers": [],
            "total_pages": 0,
        }

    if page > total_pages:
        raise PageExceedsTotalPagesError(page, total_pages)

    start = (page - 1) * page_size
    end = start + page_size

    return {
        "page": page,
        "page_size": page_size,
        "numbers": numbers[start:end],
        "total_pages": total_pages,
    }


async def add_to_blacklist(redis, n: int):
    """
    Add a number to the blacklist stored in Redis.
    """
    await redis.sadd("blacklist", n)


async def remove_from_blacklist(redis, n: int):
    """
    Remove a number from the blacklist stored in Redis.
    """
    await redis.srem("blacklist", n)


async def is_blacklisted(redis, n: int) -> bool:
    """
    Check if a number is blacklisted in Redis.
    """
    return await redis.sismember("blacklist", n)


def get_blacklist(redis_conn: Redis):
    """Fetch the blacklist from Redis."""
    return set(map(int, redis_conn.smembers("blacklist")))
