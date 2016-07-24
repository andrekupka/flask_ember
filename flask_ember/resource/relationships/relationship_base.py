from flask_ember.resource.resource_property_base import ResourcePropertyBase


class RelationshipBase(ResourcePropertyBase):
    """ Base class for relationships that target another resource.

    :param target_kind: The kind of resource that is targeted by this
                        relationship.
    :type target_kind: str or Resource
    :param backref: The name of the backward reference in the other resource.
    :type backref: str
    """

    def __init__(self, target_kind, backref):
        self.target_kind = target_kind
        self.cached_target = None

        self.backref = backref
        super().__init__()

    def register_at_descriptor(self, descriptor):
        descriptor.add_relationship(self, self.name)

    @property
    def target(self):
        if not self.cached_target:
            self.cached_target = self._resolve_target()
        return self.cached_target

    def _resolve_target(self):
        if isinstance(self.target_kind, str):
            # TODO make resolve more powerful, consider modules etc
            return self.resource._registry.resolve(self.target_kind)
        return self.target_kind
