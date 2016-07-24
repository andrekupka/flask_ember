from flask_ember.util.string import underscore

OPTIONS = [
    # the name of the generated table (is taken into account before
    # table_name_generator)
    ('table_name', None),
    # a function that takes the model class name and returns the table name
    ('table_name_generator', underscore),
    # if False a model is generate, otherwise not
    ('abstract', False)
]


class ResourceOptions:
    def __init__(self, meta=None, options=None):
        meta = meta or type('Meta', (), dict())
        options = options or OPTIONS

        for option_key, default_value in options:
            setattr(self, option_key, getattr(meta, option_key, default_value))

    def get_table_name(self, name):
        table_name = self.table_name
        if table_name is None:
            # this is save as table_name_generator has a default value
            table_name = self.table_name_generator(name)
        return table_name

    def __repr__(self):
        # TODO improve representation
        return str(self.__dict__)
