from flask_ember.dsl.class_mutator_base import ClassMutatorBase


class ResourceConfigurationMutator(ClassMutatorBase):

    def __init__(self, configurator_class):
        self.configurator_class = configurator_class
        super().__init__()

    def mutate(self, resource, *args, **kwargs):
        configurator = self.configurator_class(*args, **kwargs)
        configurator.configure(resource)
