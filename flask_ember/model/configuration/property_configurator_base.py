from abc import abstractmethod

from flask_ember.resource.configuration.resource_configurator_base import \
    ResourceConfiguratorBase


class PropertyConfiguratorBase(ResourceConfiguratorBase):
    """ A resource configurator that configures a special property of the
    resource. The property is automatically fetched from the resource's
    descriptor and configured in :meth:`configure_property` which must be
    implemented by subclasses.

    :param name: The name of the property to be configured.
    :type name: str
    """

    def __init__(self, name):
        self.name = name
        super().__init__()

    def configure(self, resource):
        """ Fetches the property with the set name from the given resource
        and delegates the property configuration to :meth:`configure_property`.

        :param resource: The resource that is to be configured.
        :type resource: FlaskEmber.Resource
        """
        prop = resource._descriptor.get_property(self.name)
        self.configure_property(prop)

    @abstractmethod
    def configure_property(self, prop):
        """ Configures the given property. Must be implemented by subclasses.

        :param prop: ResourcePropertyBase
        """
        pass
