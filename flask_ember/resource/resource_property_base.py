from abc import ABCMeta, abstractmethod


class ResourcePropertyBase(metaclass=ABCMeta):
    """ Base class for properties within resources. A property describes
    attributes or relationships of a resource. Each property has to implement
    :meth:`register_at_descriptor` which registers the property in a
    suitable way at the resource's descriptor. For generating the sqlalchemy
    model each property must implement :meth:`create_property_builder` which
    returns a :class:`flask_ember.model.PropertyBuilderBase` that is
    responsible for generating sqlalchemy columns and relationships.
    """

    def __init__(self):
        #: The resource this property is registered at.
        self.resource = None
        #: The name of this property within it's resource.
        self.name = None
        #: The builder that generates the sqlalchemy model.
        self.builder = self.create_property_builder()

    def register_at_resource(self, resource, name):
        """ Registers the property at the given resource. The registration
        at the descriptor is delegated to :meth:`register_at_descriptor`.

        :param resource: The resource to register the property at.
        :type resource: Resource
        :param name: The name of the property within the resource.
        :type name: str
        """
        self.resource = resource
        self.name = name
        self.register_at_descriptor(self.resource._descriptor)

    @abstractmethod
    def register_at_descriptor(self, descriptor):
        """ Registers this property at the given resource descriptor. This
        method must be implemented by subclasses.

        :param descriptor: The resource descriptor.
        :type descriptor: ResourceDescriptor
        """
        pass

    @abstractmethod
    def create_property_builder(self):
        """ Creates a property builder that generates the sqlalchemy model.
        This method must be implemented by subclasses.

        :rtype: PropertyBuilderBase
        """
        pass

    def get_builder(self):
        """ Returns the internally used property builder.

        :rtype: PropertyBuilderBase
        """
        return self.builder
