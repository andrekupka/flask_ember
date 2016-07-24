class CachedFunction:
    """ A cached function wraps a function and delegates calls to it. The
    wrapped function must access exactly one argument which must be hashable.
    Up to :attr:`limit` computed results of the wrapped function are cached
    in a dictionary. Thus the computation time of expensive functions without
    side effects can be optimized drastically. If the cache's limit is
    exceeded no results will be cached any longer.

    :param function: The function that is to be wrapped.
    :type function: callable
    :param limit: The maximum number of cached entries.
    :type limit: int
    """

    def __init__(self, function, limit=1000):
        #: The wrapped function.
        self.function = function
        #: The maximum number of cached results.
        self.limit = limit
        self.purge()

    def get(self, key):
        """ Returns the result of the wrapped function for the given input key.

        :param key: The input parameter.
        """
        value = self.store.get(key)
        if value is None:
            value = self.function(key)
            self.set(key, value)
        return value

    def set(self, key, value):
        """ Stores the given value for the given key in the cache and returns
        the value. If the cache limit is exceeded the value won't be stored.

        :param key: The key.
        :param value: The value.
        """
        if self.size < self.limit:
            self.size += 1
            self.store[key] = value
        return value

    def purge(self):
        """ Purges the cache and thus resets it. Therefore former computations
        have to be done again but there will be space for new ones.
        """
        self.size = 0
        self.store = dict()

    def __call__(self, key):
        """ Calls the wrapped function with the given input parameter and
        returns the result. If the cache limit is not exceeded and a cached
        result exists it will be returned instead.

        :param key: The input parameter.
        """
        return self.get(key)
