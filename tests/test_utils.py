import unittest

from app.utils import fibonacci, paginate, add_to_blacklist, is_blacklisted, remove_from_blacklist
from app.exceptions import PageExceedsTotalPagesError, InvalidPageSizeError
from redis import asyncio as aioredis


class TestFibonacci(unittest.TestCase):
    def test_fibonacci_valid_numbers(self):
        self.assertEqual(fibonacci(1), 1)
        self.assertEqual(fibonacci(2), 1)
        self.assertEqual(fibonacci(5), 5)
        self.assertEqual(fibonacci(10), 55)

    def test_fibonacci_invalid_numbers(self):
        with self.assertRaises(ValueError):
            fibonacci(0)
        with self.assertRaises(ValueError):
            fibonacci(-5)

    def test_fibonacci_large_number(self):
        self.assertEqual(fibonacci(20), 6765)


class TestPaginateFibonacci(unittest.TestCase):
    def test_paginate_fibonacci_valid(self):
        result = paginate(10, page=1, page_size=5, blacklist={2, 3})
        self.assertEqual(len(result["numbers"]), 5)
        self.assertEqual(result["total_pages"], 2)
        self.assertEqual(result["numbers"][0]["number"], 1)

    def test_paginate_fibonacci_page_bigger_than_total_pages(self):
        with self.assertRaises(PageExceedsTotalPagesError):
            paginate(10, page=11, page_size=5)

    def test_paginate_fibonacci_empty_after_blacklisting(self):
        result = paginate(10, page=1, page_size=5, blacklist=set(range(1, 11)))

        self.assertEqual(len(result["numbers"]), 0)
        self.assertEqual(result["total_pages"], 0)

    def test_paginate_fibonacci_blacklist(self):
        blacklist = {2, 3, 5, 8}
        result = paginate(10, page=1, page_size=5, blacklist=blacklist)
        self.assertEqual(len(result["numbers"]), 5)
        self.assertNotIn(2, [item["number"] for item in result["numbers"]])
        self.assertNotIn(3, [item["number"] for item in result["numbers"]])

    def test_paginate_invalid_page_size(self):
        with self.assertRaises(InvalidPageSizeError):
            paginate(10, page=5, page_size=0, blacklist=set())

    def test_paginate_default_page_size(self):
        result = paginate(10, page=1)
        self.assertEqual(result["page_size"], 10)
        self.assertEqual(len(result["numbers"]), 10)
        self.assertEqual(result["total_pages"], 1)

    def test_paginate_with_blacklist_and_default_page_size(self):
        result = paginate(10, page=1, blacklist={2, 3})
        self.assertEqual(result["page_size"], 10)
        self.assertEqual(len(result["numbers"]), 8)  # Two items blacklisted
        self.assertEqual(result["total_pages"], 1)


class TestBlacklistFunctions(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.redis = await aioredis.from_url("redis://localhost", decode_responses=True)
        await self.redis.flushall()

    async def asyncTearDown(self):
        await self.redis.aclose()

    async def test_add_to_blacklist(self):
        await add_to_blacklist(self.redis, 5)
        self.assertTrue(await is_blacklisted(self.redis, 5))

    async def test_remove_from_blacklist(self):
        await add_to_blacklist(self.redis, 5)
        await remove_from_blacklist(self.redis, 5)
        self.assertFalse(await is_blacklisted(self.redis, 5))

    async def test_check_blacklisted_number(self):
        await add_to_blacklist(self.redis, 5)
        self.assertTrue(await is_blacklisted(self.redis, 5))
        self.assertFalse(await is_blacklisted(self.redis, 10))


class TestIntegration(unittest.TestCase):
    def test_integration_fibonacci_with_blacklist(self):
        blacklist = {3, 5}
        result = paginate(10, page=1, page_size=10, blacklist=blacklist)
        self.assertEqual(len(result["numbers"]), 8)  # Total 10 numbers minus 2 blacklisted
        self.assertNotIn(3, [item["number"] for item in result["numbers"]])
        self.assertNotIn(5, [item["number"] for item in result["numbers"]])
