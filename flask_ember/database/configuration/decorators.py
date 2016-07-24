from .column_configurator import ColumnConfigurator
from .field_configurator import FieldConfigurator
from .type_configurator import TypeConfigurator


def column_config(field_name):
    def decorator(f):
        f._configurator = ColumnConfigurator(field_name, **f())
        return f

    return decorator


def field_config(field_name):
    def decorator(f):
        type_options, column_options = f()
        f._configurator = FieldConfigurator(field_name, type_options,
                                            column_options)
        return f

    return decorator


def type_config(field_name):
    def decorator(f):
        f._configurator = TypeConfigurator(field_name, **f())
        return f

    return decorator
