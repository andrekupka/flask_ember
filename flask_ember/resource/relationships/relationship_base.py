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
        :param is_many_side: Whether this side of the relationship is the many
                             side. None means that it will be determined lazily
                             while calculating the inverse relationship (this is
                             necessary for one-to-one relationships where the
                             "many"-side is the one where foreign keys are
                             generated).
        :type is_many_side: bool
        """

    def __init__(self, target_kind, backref=None, primary=None):
        self.target_kind = target_kind
        self.backref = backref
        self.primary = primary
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
        :type inverse: RelationshipBase
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
        :type other: RelationshipBase
        :rtype: bool
        """
        return isinstance(other, self.get_inverse_class())

    def is_inverse(self, other):
        """ Returns whether the given relationship is a matching inverse for
        this.

        :param other: The other relationship.
        :type other: RelationshipBase
        :rtype: bool
        """
        # 0) check that the given relation is not self
        # 1) match relation types
        # 2) match resource and target of inverse relation
        # 3) match backrefs if set
        return self is not other and \
               self.match_other(other) and \
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


    @abstractmethod
    def get_inverse_arguments(self):
        """ Returns the keyword arguments that are passed to the inverse
        relationship if one has to be created.

        :rtype: dict
        """
        pass

    def _create_inverse_relationship(self):
        """ Creates a new inverse relationship for this. The type returned
        from :meth:`get_inverse_class` is used for creation. The
        created inverse relationship is initialized with this relationship's
        resource and its name as backref. The dictionary returned from
        :meth:`get_inverse_arguments` is passed as keyword arguments.

        :rtype: RelationshipBase
        """
        inverse_class = self.get_inverse_class()
        return inverse_class(self.resource, backref=self.name,
                             **self.get_inverse_arguments())

    def check_compatibility(self, inverse):
        """ Checks whether this relationship is compatible with the given
        inverse one. If it is not an exception is to be thrown. This method
        can be overridden by subclasses.

        :param inverse: The inverse relationship.
        :type inverse: RelationshipBase
        """
        pass

    def init_inverse(self, inverse, first):
        """ Initializes the inverse relationship with the given one. If this
        relationship has no backref set it will be set now.

        :param inverse: The new inverse relationship.
        :type inverse: RelationshipBase
        :param first: Whether this side of the relationship is the one that
                      is initialized first.
        :type first: bool
        """
        self.inverse = inverse
        if self.backref is None:
            self.backref = inverse.name
        if first:
            self.configure_inverse(inverse)

    def configure_inverse(self, inverse):
        """ Configures this and the given inverse relationship. This method
        can be overridden by subclasses. This method is used to update the
        configuration of

        :param inverse: The inverse relationship.
        :type inverse: RelationshipBase
        """
        pass

    def resolve_inverse(self):
        """ Resolves the inverse relationship. If this relationship already
        has an inverse nothing is done. Otherwise the target resource is
        queried for a matching inverse relationship. If there is None a new
        inverse relationship will be created and set up at the
        target resource. If both sides have not specified whether they are
        the one or many side of the relationship, then the one that first
        resolves its inverse becomes the many side.
        """
        # If the inverse has already been set by the inverse relationship
        # there is no need for another setup round.
        if self.inverse:
            return

        inverse = self.target_descriptor.find_inverse_relationship(
            self.name, self)
        if inverse:
            self.check_compatibility(inverse)
        else:
            if self.backref is None:
                assert False, "No inverse could be determined for " \
                              "relationship '{}' in resource '{}' and there " \
                              "is no explicit backref set.".format(
                    self.name, self.resource_name)
            inverse = self._create_inverse_relationship()
            inverse.register_at_resource(self.target, self.backref)

        self.init_inverse(inverse, first=True)
        inverse.init_inverse(self, first=False)
