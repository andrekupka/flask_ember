from abc import abstractmethod
from sqlalchemy.orm import backref, relationship

from flask_ember.resource.resource_property import ResourceProperty


class RelationshipBase(ResourceProperty):

    def __init__(self, target_kind, backref=None):
        super().__init__()
        self.target_kind = target_kind
        self.cached_target = None

        self.relation = None
        self.backref = backref

    def register_at_descriptor(self, resource, name):
        super().register_at_descriptor(resource, name)
        self.descriptor.add_relationship(name, self)

    @property
    def target(self):
        if not self.cached_target:
            self.cached_target = self._resolve_target()
        return self.cached_target

    def _resolve_target(self):
        if isinstance(self.target_kind, str):
            # TODO make resolve more powerful, consider modules etc
            return self.registry.resolve(self.target_kind)
        return self.target_kind

    def create_primary_key_columns(self):
        self.create_keys(True)

    def create_non_primary_key_columns(self):
        self.create_keys(False)

    @abstractmethod
    def create_keys(self, primary_key):
        pass

    def get_relation_kwargs(self):
        back_reference = None
        if self.backref:
            back_reference = backref(self.backref, lazy='dynamic')
        return dict(
            backref=back_reference
        )

    def create_properties(self):
        if self.relation:
            return

        relation_kwargs = self.get_relation_kwargs()

        self.relation = relationship(self.target, **relation_kwargs)
        self.add_mapper_property(self.name, self.relation)
