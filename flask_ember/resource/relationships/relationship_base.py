from abc import abstractmethod
from sqlalchemy.orm import relationship

from flask_ember.resource.resource_property_base import ResourcePropertyBase


class RelationshipBase(ResourcePropertyBase):

    def __init__(self, target_kind, backref):
        super().__init__()
        self.target_kind = target_kind
        self.cached_target = None

        self.relation = None
        self.backref = backref

        self.primary_join_clauses = list()

    def register_at_descriptor(self, resource, name):
        super().register_at_descriptor(resource, name)
        self.descriptor.add_relationship(name, self)

    @property
    def target(self):
        if not self.cached_target:
            self.cached_target = self._resolve_target()
        return self.cached_target

    @property
    def target_table(self):
        return self.target._table

    def _resolve_target(self):
        if isinstance(self.target_kind, str):
            # TODO make resolve more powerful, consider modules etc
            return self.registry.resolve(self.target_kind)
        return self.target_kind

    @abstractmethod
    def get_relation_kwargs(self):
        pass

    def create_properties(self):
        if self.relation:
            return

        relation_kwargs = self.get_relation_kwargs()

        self.relation = relationship(self.target, **relation_kwargs)
        self.add_mapper_property(self.name, self.relation)
