from .resource_builder import ResourceBuilder


class ResourceProperty(ResourceBuilder):

    def __init__(self):
        self.resource = None
        self.name = None

    def register_at_descriptor(self, resource, name):
        self.resource = resource
        self.name = name
        self.descriptor.add_builder(self)

    def add_table_column(self, column):
        self.descriptor.add_column(column)

    def add_mapper_property(self, name, prop):
        self.descriptor.add_property(name, prop)

    @property
    def registry(self):
        assert self.resource is not None, 'Resource must be attached'
        return self.resource._registry

    @property
    def descriptor(self):
        assert self.resource is not None, 'Resource must be attached'
        return self.resource._descriptor
