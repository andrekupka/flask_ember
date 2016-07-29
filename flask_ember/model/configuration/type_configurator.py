from .field_configurator import FieldConfigurator


class TypeConfigurator(FieldConfigurator):
    """ A resource property configurator that configures the sqlalchemy
    type of a field property.

    :param name: The name of the property to be configured.
    :type name: str
    :param type_options: Options that configure the sqlalchemy type.
    :type type_options: dict
    """

    def __init__(self, name, **type_options):
        super().__init__(name, type=type_options)
