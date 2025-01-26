from app.exceptions import InvalidNumberError


def fibonacci(n: int) -> int:
    """Calculate Fibonacci the iterative way instead of recursive, for improvements."""
    if n <= 0:
        raise InvalidNumberError(n)
    if n == 1 or n == 2:
        return 1

    a, b = 1, 1
    for _ in range(2, n):
        a, b = b, a + b

    return b


def paginate(n: int, page: int, page_size: int = 10, blacklist: set = None):
    if page_size <= 0:
        raise ValueError("Page size must be a positive integer.")
    if page <= 0:
        raise ValueError("Page number must be a positive integer.")
    if n <= 0:
        raise ValueError("Total number of Fibonacci numbers must be a positive integer.")

    if blacklist is None:
        blacklist = set()

    numbers = []
    for i in range(1, n + 1):
        if i not in blacklist:
            numbers.append({"number": i, "fibonacci": fibonacci(i)})

    total_pages = (len(numbers) + page_size - 1) // page_size

    if len(numbers) == 0:
        return {
            "page": page,
            "page_size": page_size,
            "numbers": [],
            "total_pages": 0,
        }

    if page > total_pages:
        raise ValueError(f"Page number {page} exceeds total pages {total_pages}.")

    start = (page - 1) * page_size
    end = start + page_size
    current_page_numbers = numbers[start:end]

    return {
        "page": page,
        "page_size": page_size,
        "numbers": current_page_numbers,
        "total_pages": total_pages,
    }
