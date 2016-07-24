from .property_configurator import PropertyConfigurator


class ColumnConfigurator(PropertyConfigurator):
    def __init__(self, name, **column_options):
        self.column_options = column_options
        super().__init__(name)

    def configure_property(self, prop):
        print("Configuring column for %s" % self.name)
        prop.get_builder().override_column_options(self.column_options)
