from abc import ABCMeta, abstractmethod


class ResourceConfiguratorBase(metaclass=ABCMeta):
    """ Base class for resources configurators. A resource configurator
    configures parts of a resource class. This is done by implementing and
    calling :meth:`configure`. Configurators are normally attached to a
    field of the resource class. Therefor they are stored in a list that is
    accessible through :const:`KEY`.
    """

    #: The key that is used to attach configurators to a resource class
    #: member.
    KEY = '_configurators'

    @abstractmethod
    def configure(self, resource):
        """ Configures the given resource class. Must be implemented by
        subclasses.

        :param resource: The resource class that is to be configured.
        :type resource: FlaskEmber.Resource
        """
        pass

    @staticmethod
    def apply_configurators(resource):
        """ Applies all configurators that are registered at the given
        resource and removes them.

        :param resource: The resource class that is to be configured.
        :type resource: FlaskEmber.Resource
        """
        for name, attr in list(resource.__dict__.items()):
            configurators = getattr(attr, ResourceConfiguratorBase.KEY, [])
            for configurator in configurators:
                configurator.configure(resource)
            if configurators:
                delattr(attr, ResourceConfiguratorBase.KEY)

    @staticmethod
    def attach_configurator(attribute, configurator):
        """ Attaches the given configurator at the given attribute.

        :param attribute: The attribute to attach to.
        :type attribute: object
        :param configurator: The configuration to be attached.
        :type configurator: ResourceConfiguratorBase
        """
        configurators = attribute.__dict__.setdefault(
            ResourceConfiguratorBase.KEY, [])
        configurators.append(configurator)
