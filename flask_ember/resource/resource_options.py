from flask_ember.util.string import underscore


OPTIONS = [
    # the name of the generated table (is taken into account before
    # tablename_generator)
    ('tablename', None),
    # a function that takes the model class name and returns the table name
    ('tablename_generator', underscore),
    # if False a model is generate, otherwise not
    ('abstract', False)
]


class ResourceOptions:
    def __init__(self, meta=None, options=None):
        meta = meta or type('Meta', (), dict())
        options = options or OPTIONS

        for option_key, default_value in options:
            setattr(self, option_key, getattr(meta, option_key, default_value))

    def get_tablename(self, name):
        tablename = self.tablename
        if tablename is None:
            # this is save as tablename_function has a default value
            tablename = self.tablename_generator(name)
        return tablename

    def __repr__(self):
        # TODO improve representation
        return str(self.__dict__)
