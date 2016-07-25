from abc import ABCMeta, abstractmethod
import sys


class ClassMutatorBase(metaclass=ABCMeta):
    """ Base class for a class mutator which is used for declaring DSL-like
    function that are callable within a classes scope and mutate the
    respective class. The function call registers the mutator at the class
    while evaluating it. Afterwards all mutators can be applied to a class
    using :meth:`apply_mutators`. In most cases this is done by a metaclass.
    """

    #: The key that is used to store mutators as attribute in an class'
    #: dictionary.
    KEY = '__mutators__'

    def __call__(self, *args, **kwargs):
        """ Registers the this mutator in the surrounding class' dictionary.
        The mutator is stored in a list in the resource's dictionary that is
        accessible by :const:`KEY`. All passed arguments are forwarded to
        :meth:`mutate`.

        :param args: Positional arguments that are stored with the mutator
                     and forwarded to :meth:`mutate`.
        :param kwargs: Keyword arguments that are stored with the mutator
                       and forwarded to :meth:`mutate`.
        """
        class_locals = sys._getframe(1).f_locals
        mutators = class_locals.setdefault(ClassMutatorBase.KEY, [])
        mutators.append((self, args, kwargs))

    @abstractmethod
    def mutate(self, cls, *args, **kwargs):
        """ Mutates the given class.

        :param cls: The class that is to be mutated.
        :param args: Positional arguments that where passed to the mutators
                     call.
        :param kwargs: Keyword arguments that where passed to the mutators
                       call.
        """
        pass

    @staticmethod
    def apply_mutators(cls):
        """ Applies all mutators that are registered at the given class to it.

        :param cls: The class to apply mutators to.
        :type cls: type
        """

        # getattr is explicitly not used as this would inherit mutators
        # from parent classes.
        mutators = cls.__dict__.get(ClassMutatorBase.KEY, [])
        for mutator, args, kwargs in mutators:
            mutator.mutate(cls, *args, **kwargs)
        # TODO delete __mutators__ from the class after processing them
