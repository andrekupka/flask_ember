from flask_ember.model.many_to_many_relationship_builder import \
    ManyToManyRelationshipBuilder
from .relationship_base import RelationshipBase


class ManyToMany(RelationshipBase):
    def __init__(self, target_kind, **kwargs):
        self.association_table = None
        super().__init__(target_kind, is_many_side=True, **kwargs)

    def create_builder(self):
        return ManyToManyRelationshipBuilder(resource_property=self)

    def get_inverse_class(self):
        return ManyToMany
