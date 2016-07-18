import unittest

from flask_ember.util.cache import Cache


class CacheTestCase(unittest.TestCase):

    def test_basic(self):
        cache = Cache(lambda x: x * 2)
        self.assertEqual(cache.get(1), 2)

    def test_caching(self):
        calculations = 0

        def cache_function(value):
            nonlocal calculations
            calculations += 1
            return value * 2

        function = Cache(cache_function)

        self.assertEqual(function(2), 4)
        self.assertEqual(function(2), 4)
        self.assertEqual(calculations, 1)
