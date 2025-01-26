class PaginationError(ValueError):
    pass


class InvalidNumberError(ValueError):
    def __init__(self, number: int):
        super().__init__(f"Fibonacci number {number} must be a positive integer.")
        self.number = number


class PageExceedsTotalPagesError(PaginationError):
    def __init__(self, page: int, total_pages: int):
        super().__init__(f"Page {page} exceeds the total number of pages ({total_pages}).")
        self.page = page
        self.total_pages = total_pages


class InvalidPageSizeError(PaginationError):
    def __init__(self, page_size: int):
        super().__init__(f"Page size must be a positive integer. Received: {page_size}.")
        self.page_size = page_size


class InvalidPageNumberError(PaginationError):
    def __init__(self, page: int):
        super().__init__(f"Page number must be a positive integer. Received: {page}.")
        self.page = page


class InvalidTotalItemsError(PaginationError):
    def __init__(self, n: int):
        super().__init__(f"The total number of items must be a positive integer. Received: {n}.")
        self.n = n
