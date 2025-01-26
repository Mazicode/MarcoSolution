import unittest

import pytest

from app.utils import fibonacci, paginate


class TestFibonacci(unittest.TestCase):
    def test_fibonacci_valid_input(self):
        self.assertEqual(fibonacci(1), 1)
        self.assertEqual(fibonacci(2), 1)
        self.assertEqual(fibonacci(3), 2)
        self.assertEqual(fibonacci(4), 3)
        self.assertEqual(fibonacci(5), 5)
        self.assertEqual(fibonacci(6), 8)

    def test_fibonacci_large_input(self):
        self.assertEqual(fibonacci(10), 55)

    def test_fibonacci_invalid_input(self):
        with self.assertRaises(ValueError):
            fibonacci(0)
        with self.assertRaises(ValueError):
            fibonacci(-5)


def test_paginate():
    result = paginate(10, 1, page_size=3)
    assert result["page"] == 1
    assert result["page_size"] == 3
    assert len(result["numbers"]) == 3
    assert result["numbers"] == [
        {"number": 1, "fibonacci": fibonacci(1)},
        {"number": 2, "fibonacci": fibonacci(2)},
        {"number": 3, "fibonacci": fibonacci(3)},
    ]
    assert result["total_pages"] == 4

    result = paginate(10, 1, page_size=5, blacklist={2, 4, 6})
    assert len(result["numbers"]) == 5
    assert all(num["number"] not in {2, 4, 6} for num in result["numbers"])
    assert result["total_pages"] == 2

    with pytest.raises(ValueError, match="Page size must be a positive integer."):
        paginate(10, 1, page_size=0)

    with pytest.raises(ValueError, match="Page number must be a positive integer."):
        paginate(10, 0, page_size=3)

    with pytest.raises(ValueError, match="Total number of Fibonacci numbers must be a positive integer."):
        paginate(-1, 1, page_size=3)

    with pytest.raises(ValueError, match="Page number 5 exceeds total pages 4."):
        paginate(10, 5, page_size=3)

    result = paginate(10, 1, page_size=5, blacklist=set(range(1, 11)))
    assert result["numbers"] == []
    assert result["total_pages"] == 0
    assert result["page"] == 1


if __name__ == "__main__":
    unittest.main()
