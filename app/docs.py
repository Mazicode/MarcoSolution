from app.schemas import FibonacciResponse, FibonacciListResponse, BlacklistResponse

FIBONACCI_DOCS = {
    "summary": "Get Fibonacci Number",
    "description": "Returns the Fibonacci number for a given positive integer `number`. "
                   "If the number is blacklisted, the request will be rejected.",
    "responses": {
        200: {
            "description": "The Fibonacci number for the given input.",
            "model": FibonacciResponse,
        },
        400: {
            "description": "The requested number is blacklisted or invalid input.",
            "content": {
                "application/json": {
                    "example": {"detail": "Number is blacklisted."}
                }
            },
        },
    },
}

FIBONACCI_LIST_DOCS = {
    "summary": "Get Paginated Fibonacci Numbers",
    "description": "Returns a paginated list of Fibonacci numbers (excluding blacklisted numbers). "
                   "Pagination is controlled via `page` and `page_size` query parameters. "
                   "The numbers are paginated starting from the first Fibonacci number up to `n`.",
    "responses": {
        200: {
            "description": "The paginated list of Fibonacci numbers.",
            "model": FibonacciListResponse,
        },
        400: {
            "description": "Invalid pagination or other input errors, such as non-positive integers for `n`, `page`, or `page_size`.",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid page size or max_n."}
                }
            },
        },
    },
}

BLACKLIST_ADD_DOCS = {
    "summary": "Add Number to Blacklist",
    "description": "Adds a given number to the blacklist. Blacklisted numbers cannot be requested in Fibonacci endpoints.",
    "responses": {
        200: {
            "description": "Confirmation that the number has been blacklisted.",
            "model": BlacklistResponse,
        },
        400: {
            "description": "Invalid input (e.g., non-positive integer for `number`).",
            "content": {
                "application/json": {
                    "example": {"detail": "Input must be a positive integer."}
                }
            },
        },
    },
}

BLACKLIST_REMOVE_DOCS = {
    "summary": "Remove Number from Blacklist",
    "description": "Removes a given number from the blacklist. Blacklisted numbers can then be requested again.",
    "responses": {
        200: {
            "description": "Confirmation that the number has been removed from the blacklist.",
            "model": BlacklistResponse,
        },
        404: {
            "description": "The given number is not in the blacklist.",
            "content": {
                "application/json": {
                    "example": {"detail": "Number 3 is not in the blacklist."}
                }
            },
        },
    },
}
