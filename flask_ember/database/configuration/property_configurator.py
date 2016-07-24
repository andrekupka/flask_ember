from abc import abstractmethod

from flask_ember.resource.configuration.resource_configurator_base import \
    ResourceConfiguratorBase


class PropertyConfigurator(ResourceConfiguratorBase):
    def __init__(self, name):
        self.name = name
        super().__init__()

    def configure(self, cls):
        prop = cls._descriptor.get_property(self.name)
        self.configure_property(prop)

    @abstractmethod
    def configure_property(self, prop):
        pass
