import flask_ember.resource.relationships
from flask_ember.model.relationship_builder import RelationshipBuilder
from .one_sided_relationship_base import OneSidedRelationshipBase


class ManyToOne(OneSidedRelationshipBase):
    def __init__(self, target_kind, **kwargs):
        super().__init__(target_kind, is_many_side=True, **kwargs)

    def create_builder(self):
        return RelationshipBuilder(use_list=False, resource_property=self)

    def get_inverse_class(self):
        return flask_ember.resource.relationships.OneToMany
