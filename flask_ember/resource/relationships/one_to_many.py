import flask_ember.resource.relationships
from flask_ember.model.one_sided_relationship_builder import \
    OneSidedRelationshipBuilder
from .relationship_base import RelationshipBase


class OneToMany(RelationshipBase):
    def __init__(self, target_kind, **kwargs):
        super().__init__(target_kind, is_many_side=False, **kwargs)

    def create_builder(self):
        return OneSidedRelationshipBuilder(use_list=True,
                                           resource_property=self)

    def get_inverse_class(self):
        return flask_ember.resource.relationships.ManyToOne
