from abc import ABCMeta, abstractmethod


class ResourceConfiguratorBase(metaclass=ABCMeta):
    @abstractmethod
    def configure(self, cls):
        pass

    @staticmethod
    def apply_configurators(resource):
        for name, attr in list(resource.__dict__.items()):
            if hasattr(attr, '_configurator'):
                attr._configurator.configure(resource)
                delattr(attr, '_configurator')
