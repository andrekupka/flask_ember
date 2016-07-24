from abc import ABCMeta, abstractmethod
import sys


class ResourceMutator(metaclass=ABCMeta):
    """ A resource mutator is used for declaring DSL-like function calls
    within a resource's class scope. The function call registers the mutator at
    the resource while evaluating the resource's class. Afterwards all
    mutators can be applied to a resource class using
    :meth:`apply_mutators`. This is done by the metaclass of the resource.
    """

    #: The key that is used to store mutators as attribute in an resource.
    KEY = '__mutators__'

    def __call__(self, *args, **kwargs):
        """ Registers the this mutator in the surrounding resource's
        dictionary. The mutator is stored in a list in the resource's
        dictionary that is accessible by :const:`KEY`. All passed arguments
        are forwarded to :meth:`mutate`.

        :param args: Positional arguments that are stored with the mutator
                     and forwarded to :meth:`mutate`.
        :param kwargs: Keyword arguments that are stored with the mutator
                       and forwarded to :meth:`mutate`.
        """
        class_locals = sys._getframe(1).f_locals
        mutators = class_locals.setdefault(ResourceMutator.KEY, [])
        mutators.append((self, args, kwargs))

    @abstractmethod
    def mutate(self, resource, *args, **kwargs):
        """ Mutates the given resource.

        :param resource: The resource that is to be mutated.
        :param args: Positional arguments that where passed to the mutators
                     call.
        :param kwargs: Keyword arguments that where passed to the mutators
                       call.
        """
        pass

    @staticmethod
    def apply_mutators(resource):
        """ Applies all mutators that are registered at the given resource
        to the resource.

        :param resource: The resource to apply mutators to.
        """

        # getattr is explicitly not used as this would inherit mutators
        # from parent classes.
        mutators = resource.__dict__.get(ResourceMutator.KEY, [])
        for mutator, args, kwargs in mutators:
            mutator.mutate(resource, *args, **kwargs)
        # TODO delete __mutators__ from the resource after processing them
