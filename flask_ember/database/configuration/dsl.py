from flask_ember.resource.configuration.resource_configuration_mutator import \
    ResourceConfigurationMutator
from .column_configurator import ColumnConfigurator
from .field_configurator import FieldConfigurator
from .type_configurator import TypeConfigurator


configure_column = ResourceConfigurationMutator(ColumnConfigurator)
configure_field = ResourceConfigurationMutator(FieldConfigurator)
configure_type = ResourceConfigurationMutator(TypeConfigurator)
