class ResourceOptions:

    def __init__(self, meta=None):
        meta = meta or type('Meta', (), dict())

        self.tablename = getattr(meta, 'tablename', None)

    def __repr__(self):
        return str(self.__dict__)
