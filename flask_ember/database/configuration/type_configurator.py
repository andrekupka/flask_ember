from .property_configurator import PropertyConfigurator


class TypeConfigurator(PropertyConfigurator):
    def __init__(self, name, **type_options):
        self.type_options = type_options
        super().__init__(name)

    def configure_property(self, prop):
        print("Configuring type for %s" % self.name)
        prop.get_builder().override_type_options(self.type_options)
