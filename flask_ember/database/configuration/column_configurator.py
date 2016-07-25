from .field_configurator import FieldConfigurator


class ColumnConfigurator(FieldConfigurator):
    """ A resource property configurator that configures the sqlalchemy
    column of an attribute property.

    :param name: The name of the property to be configured.
    :type name: str
    :param column_options: Options that configure the sqlalchemy column.
    :type column_options: dict
    """

    def __init__(self, name, **column_options):
        super().__init__(name, column=column_options)
