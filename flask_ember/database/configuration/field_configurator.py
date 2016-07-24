from .property_configurator import PropertyConfigurator


class FieldConfigurator(PropertyConfigurator):
    def __init__(self, name, type=None, column=None):
        self.type_options = type or dict()
        self.column_options = column or dict()
        super().__init__(name)

    def configure_property(self, prop):
        print("Configuring field for %s" % self.name)
        builder = prop.get_builder()
        builder.override_column_options(self.column_options)
        builder.override_type_options(self.type_options)
