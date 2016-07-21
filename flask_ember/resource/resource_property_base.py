from abc import ABCMeta, abstractmethod


class ResourcePropertyBase(metaclass=ABCMeta):

    def __init__(self):
        self.resource = None
        self.name = None
        self.builder = self.create_property_builder()

    def register_at_descriptor(self, resource, name):
        self.resource = resource
        self.name = name
        self.do_register_at_descriptor(self.resource._descriptor)

    @abstractmethod
    def do_register_at_descriptor(self, descriptor):
        pass

    @abstractmethod
    def create_property_builder(self):
        pass

    def get_builder(self):
        return self.builder

    @property
    def registry(self):
        assert self.resource is not None, 'Resource must be attached'
        return self.resource._registry

    @property
    def table(self):
        assert self.resource is not None, 'Resource must be attached'
        return self.resource._table
