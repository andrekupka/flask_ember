from .resource_builder import ResourceBuilder


class ResourceProperty(ResourceBuilder):

    def __init__(self):
        self.resource = resource
        self.name = None

    def register_at_descriptor(self, resource, name):
        self.resource = resource
        self.name = name
        resource._descriptor.add_builder(self)
