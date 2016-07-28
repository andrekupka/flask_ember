from abc import abstractmethod

from flask_ember.resource.resource_property_base import ResourcePropertyBase


class RelationshipBase(ResourcePropertyBase):
    """ Base class for relationships that target another resource.

        :param target_kind: The kind of resource that is targeted by this
                            relationship.
        :type target_kind: str or Resource
        :param backref: The name of the backward reference in the other
                        resource. If the backref is None a unique matching
                        inverse relationship must exist in the target resource.
        :type backref: str
        """

    def __init__(self, target_kind, backref=None):
        self.target_kind = target_kind
        self.backref = backref
        self._target = None
        self._inverse = None
        super().__init__()

    def register_at_descriptor(self, descriptor):
        descriptor.add_relationship(self, self.name)

    @property
    def target(self):
        """ The target resource of the relationship.
        """
        if not self._target:
            self._target = self._resolve_target()
        return self._target

    @property
    def target_descriptor(self):
        """ The descriptor of the target resource of the relationship.
        """
        return self.target._descriptor

    @property
    def inverse(self):
        """ The inverse relationship. Can be None if
        :meth:`resolve_inverse` has not yet been called.
        """
        return self._inverse

    @inverse.setter
    def inverse(self, inverse):
        """ Sets the inverse relationship. If it has already been set an
        assertion is triggered.

        :param inverse: The new inverse relationship.
        :type inverse: SingleSidedRelationshipBase
        """
        assert not self.inverse, ("Relationship '{}' in resource '{}' already "
                                  "has a inverse relationship set.".format(
            self.name, self.resource_name))
        self._inverse = inverse

    @abstractmethod
    def get_inverse_class(self):
        """ Returns the matching inverse relationship class. This method
        must be implemented by concrete relationship classes and must return a
        subclass of :class:`RelationshipBase`.

        :rtype: type
        """
        pass

    def match_other(self, other):
        """ Returns whether this relationship is matching the other
        relationship class. Therefore the other relationship must be an
        instance of the type returned by :meth:`get_inverse_class`.

        :param other: The other relationship.
        :type other: SingleSidedRelationshipBase
        :rtype: bool
        """
        return isinstance(other, self.get_inverse_class())

    def is_inverse(self, other):
        """ Returns whether the given relationship is a matching inverse
        for this.

        :param other: The other relationship.
        :type other: SingleSidedRelationshipBase
        :rtype: bool
        """
        # 1) match relation types
        # 2) match resource and target of inverse relation
        # 3) match backrefs if set
        return self.match_other(other) and \
               self.resource == other.target and \
               self.target == other.resource and \
               (self.backref is None or self.backref == other.name) and \
               (other.backref is None or other.backref == self.name)

    def matching_backref_exists(self, other):
        """ Returns whether this and the given relationship have a matching
        backref in at least one direction.

        :param other: The other relationship.
        :rtype: bool
        """
        return self.backref == other.name or other.backref == self.name

    def _resolve_target(self):
        """ Resolves the target resource depending on :attr:`target_kind`.
        If it is a string a lookup in the resource registry will be done,
        otherwise :attr:`target_kind` will be used directly.

        :rtype: Resource
        """
        if isinstance(self.target_kind, str):
            # TODO make resolve more powerful, consider modules etc
            return self.resource._registry.resolve(self.target_kind)
        return self.target_kind
