from .relationship_base import RelationshipBase


class OneSidedRelationshipBase(RelationshipBase):
    """ Base class for relationships that target another resource and have
    at least one one side. This includes one-to-many, many-to-one and
    one-to-one relationships.

    :param target_kind: The kind of resource that is targeted by this
                        relationship.
    :type target_kind: str or Resource
                    resource. If the backref is None a unique matching
                    inverse relationship must exist in the target resource.
    :type backref: str
    :param kwargs: Keyword arguments that are passed to the constructor of
                   the base class.
    """

    def __init__(self, target_kind, is_many_side=None, **kwargs):
        self.is_many_side = is_many_side
        super().__init__(target_kind, **kwargs)

    def _create_inverse_relationship(self):
        """ Creates a new inverse relationship for this. The type returned
        from :meth:`get_inverse_class` is used for creation.

        :rtype: OneSidedRelationshipBase
        """
        inverse_class = self.get_inverse_class()
        return inverse_class(self.resource, backref=self.name)

    def init_inverse(self, inverse, is_many_side):
        """ Initializes the inverse relationship with the given one. If this
        relationship has no backref set it will be set now. If this
        relationship has not yet determined whether it is the one or many side,
        it will be set to the given value.

        :param inverse: The new inverse relationship.
        :type inverse: OneSidedRelationshipBase
        :param is_many_side: Whether this relationship may be the many side.
        :type is_many_side: bool
        """
        self.inverse = inverse
        if self.backref is None:
            self.backref = inverse.name
        if self.is_many_side is None:
            self.is_many_side = is_many_side

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
        if not inverse:
            if self.backref is None:
                # TODO error if no inverse was found automatically
                assert False, "No inverse could be determined for " \
                              "relationship '{}' in resource '{}' and there " \
                              "is no explicit backref set.".format(
                    self.name, self.resource_name)
            inverse = self._create_inverse_relationship()
            inverse.register_at_resource(self.target, self.backref)

        self.init_inverse(inverse, is_many_side=True)
        inverse.init_inverse(self, is_many_side=False)
