from .resource_options import ResourceOptions
from flask_ember.model.model_builder import ModelBuilder


class ResourceDescriptor:

    def __init__(self, resource):
        self.resource = resource
        self.model_builder = ModelBuilder(resource)
        self.options = ResourceOptions(resource.__dict__.get('Meta', None))

        self.fields = dict()
        self.relationships = dict()

    def add_field(self, field, name):
        if name in self.fields:
            raise Exception("Field '{}' already exists in resource "
                            "'{}'.".format(name, self.resource_name))
        self.fields[name] = field
        self.model_builder.add_builder(field.get_builder())

    def call_model_builder(self, operation):
        if hasattr(self.model_builder, operation):
            getattr(self.model_builder, operation)()

    @property
    def resource_name(self):
        return self.resource.__name__

    def __repr__(self):
        # TODO improve representation
        return str(self.__dict__)
