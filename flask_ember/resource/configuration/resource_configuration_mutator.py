from flask_ember.dsl.resource_mutator import ResourceMutator


class ResourceConfigurationMutator(ResourceMutator):

    def __init__(self, configurator_class):
        self.configurator_class = configurator_class
        super().__init__()

    def mutate(self, resource, *args, **kwargs):
        configurator = self.configurator_class(*args, **kwargs)
        configurator.configure(resource)
