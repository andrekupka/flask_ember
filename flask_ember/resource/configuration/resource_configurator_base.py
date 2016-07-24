from abc import ABCMeta, abstractmethod


class ResourceConfiguratorBase(metaclass=ABCMeta):

    @abstractmethod
    def configure(self, cls):
        pass
