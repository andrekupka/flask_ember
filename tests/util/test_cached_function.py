import unittest

from flask_ember.util.cached_function import CachedFunction


class CacheTestCase(unittest.TestCase):

    def test_basic(self):
        function = CachedFunction(lambda x: x * 2)
        self.assertEqual(function.get(1), 2)

    def test_caching(self):
        calculations = 0

        def cache_function(value):
            nonlocal calculations
            calculations += 1
            return value * 2

        function = CachedFunction(cache_function)

        self.assertEqual(function(2), 4)
        self.assertEqual(function(2), 4)
        self.assertEqual(calculations, 1)
