from flask_ember.dsl.class_mutator_base import ClassMutatorBase


class ResourceConfigurationMutator(ClassMutatorBase):
    """ A resource configuration mutator is a class mutator that wraps a
    :class:`flask_ember.resource.configuration.ResourceConfiguratorBase`
    into a DSL-like function. All arguments that are passed to the mutator
    are forwarded to the constructor of the resource configurator.

    :param configurator_class: The class of the configurator that is to be
                               wrapped.
    :type configurator_class: type
    """

    def __init__(self, configurator_class):
        self.configurator_class = configurator_class
        super().__init__()

    def mutate(self, resource, *args, **kwargs):
        """ Instantiates the wrapped configurator with the given positional
        and keyword arguments and configures the given resource with it.

        :param resource: The resource that is to be configured.
        :type resource: FlaskEmber.Resource
        :param args: The positional arguments.
        :param kwargs: The keyword arguments.
        """
        configurator = self.configurator_class(*args, **kwargs)
        configurator.configure(resource)
