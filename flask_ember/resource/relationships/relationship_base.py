from abc import abstractmethod

from flask_ember.resource.resource_property_base import ResourcePropertyBase


class RelationshipBase(ResourcePropertyBase):
    """ Base class for relationships that target another resource.

    :param target_kind: The kind of resource that is targeted by this
                        relationship.
    :type target_kind: str or Resource
    :param backref: The name of the backward reference in the other resource.
    :type backref: str
    :param is_many_side: Whether this side of the relationship is the many
                         side. None means that it will be determined lazily
                         while calculating the inverse relationship (this is
                         necessary for one-to-one relationships where the
                         "many"-side is the one where foreign keys are
                         generated).
    :type is_many_side: bool
    """

    def __init__(self, target_kind, backref, is_many_side=None):
        self.target_kind = target_kind
        self.backref = backref
        self.is_many_side = is_many_side
        self._target = None
        self._inverse = None
        super().__init__()

    def register_at_descriptor(self, descriptor):
        descriptor.add_relationship(self, self.name)

    @abstractmethod
    def get_inverse_class(self):
        pass

    def match_other(self, other):
        return isinstance(other, self.get_inverse_class())

    def create_inverse_relationship(self):
        inverse_class = self.get_inverse_class()
        return inverse_class(self.resource, self.name)

    @property
    def target(self):
        if not self._target:
            self._target = self._resolve_target()
        return self._target

    @property
    def target_descriptor(self):
        return self.target._descriptor

    @property
    def inverse(self):
        return self._inverse

    @inverse.setter
    def inverse(self, inverse):
        assert not self.inverse, ("Relationship '{}' already has a reverse "
                                  "relationship set.".format(self.name))
        self._inverse = inverse

    def setup_inverse(self, inverse, is_many_side):
        self.inverse = inverse
        if self.is_many_side is None:
            self.is_many_side = is_many_side

    def resolve_inverse_relationships(self):
        # If the inverse has already been set by the inverse relationship
        # there is no need for another setup round.
        if self.inverse:
            return

        inverse = self.target_descriptor.find_inverse_relationship(
            self.name, self)
        if not inverse:
            inverse = self.create_inverse_relationship()
            inverse.register_at_resource(self.target, self.backref)

        self.setup_inverse(inverse, is_many_side=True)
        inverse.setup_inverse(self, is_many_side=False)

    def _resolve_target(self):
        if isinstance(self.target_kind, str):
            # TODO make resolve more powerful, consider modules etc
            return self.resource._registry.resolve(self.target_kind)
        return self.target_kind
