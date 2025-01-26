import unittest

from app.utils import fibonacci


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


if __name__ == "__main__":
    unittest.main()
