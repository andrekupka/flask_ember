from flask_ember.resource.configuration.resource_configurator_base import \
    ResourceConfiguratorBase
from .column_configurator import ColumnConfigurator
from .field_configurator import FieldConfigurator
from .type_configurator import TypeConfigurator


# TODO The configuration decorators are currently attached to static methods as
# these are directly called in the decorator in order to obtain the
# configuration parameters. Thus an additional @staticmethod decorator would
# be necessary which would bloat up the code a bit. Leaving it away is rather
# ugly as well.
# Another option would be declaring the decorated method as instance methods
# and passing None to the call in the decorator. This feels really wrong.
# Currently I prefer the @staticmethod option.


def column_config(*field_names):
    def decorator(f):
        for field_name in field_names:
            configurator = ColumnConfigurator(field_name, **f())
            ResourceConfiguratorBase.attach_configurator(f, configurator)
        return f

    return decorator


def field_config(*field_names):
    def decorator(f):
        for field_name in field_names:
            configurator = FieldConfigurator(field_name, *f())
            ResourceConfiguratorBase.attach_configurator(f, configurator)
        return f

    return decorator


def type_config(*field_names):
    def decorator(f):
        for field_name in field_names:
            configurator = TypeConfigurator(field_name, **f())
            ResourceConfiguratorBase.attach_configurator(f, configurator)
        return f

    return decorator
