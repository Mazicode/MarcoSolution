def fibonacci(n: int) -> int:
    if n <= 0:
        raise ValueError("Fibonacci number must be a positive integer.")
    if n == 1 or n == 2:
        return 1

    return fibonacci(n - 1) + fibonacci(n - 2)
