from .property_configurator_base import PropertyConfiguratorBase


class FieldConfigurator(PropertyConfiguratorBase):
    """ A resource property configurator that configures the sqlalchemy type
    and column of a field property.

    :param name: The name of the property to be configured.
    :type name: str
    :param type: Options that configure the sqlalchemy type.
    :type type: dict
    :param column: Options that configure the sqlalchemy column.
    :type column: dict
    """

    def __init__(self, name, type=None, column=None):
        self.type_options = type or dict()
        self.column_options = column or dict()
        super().__init__(name)

    def configure_property(self, prop):
        """ Merges the type and column options into the builder of the
        given property.

        :param prop: The property to be configured.
        :type prop: ResourcePropertyBase
        """
        builder = prop.get_builder()
        builder.override_column_options(self.column_options)
        builder.override_type_options(self.type_options)
