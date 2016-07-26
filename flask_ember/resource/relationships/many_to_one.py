import flask_ember.resource.relationships
from flask_ember.model.relationship_builder import RelationshipBuilder
from .relationship_base import RelationshipBase


class ManyToOne(RelationshipBase):
    def __init__(self, target_kind, backref):
        super().__init__(target_kind, backref, is_many_side=True)

    def create_property_builder(self):
        return RelationshipBuilder(self.backref, use_list=False,
                                   resource_property=self)

    def match_other(self, other):
        return isinstance(other, flask_ember.resource.relationships.OneToMany)

    def get_inverse_class(self):
        return flask_ember.resource.relationships.OneToMany
