class Cache:
    def __init__(self, function, limit=1000):
        self.function = function
        self.limit = limit
        self.purge()

    def get(self, key):
        value = self.store.get(key)
        if value is None:
            value = self.function(key)
            self.set(key, value)
        return value

    def set(self, key, value):
        if self.size < self.limit:
            self.size += 1
            self.store[key] = value
        return value

    def purge(self):
        self.size = 0
        self.store = dict()

    def __call__(self):
        return lambda key: self.get(key)
