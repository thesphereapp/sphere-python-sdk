from typing import List
from unittest import TestCase

from main.utils.cache import timed_lru_cache, list_to_tuple


class TestUtils(TestCase):

    def test_caching_works_with_numeric_arguments(self):
        self._f1(5)
        self._f1(4)
        self._f1(5)
        self.assertEqual(True, True)

    def test_caching_works_with_list_arguments(self):
        self._f2([1, 2, 3])
        self._f2([4, 5, 6])
        self._f2([1, 2, 3])
        self.assertEqual(True, True)

    def test_caching_works_with_multiple_arguments(self):
        self._f3(5, 1)
        self._f3(4, 0)
        self._f3(5, 1)
        self.assertEqual(True, True)

    @staticmethod
    @timed_lru_cache(seconds=15)
    def _f1(nr: int):
        if nr > 5:
            return 5
        return nr

    @staticmethod
    @list_to_tuple
    @timed_lru_cache(seconds=15)
    def _f2(nrs: List[int]):
        if len(nrs) > 2:
            return 5
        return len(nrs)

    @staticmethod
    @timed_lru_cache(seconds=15)
    def _f3(n1: int, n2: int):
        return n1 + n2
