from flask_ember.model.relationship_builder import RelationshipBuilder
from .relationship_base import RelationshipBase


class OneToMany(RelationshipBase):
    def create_property_builder(self):
        return RelationshipBuilder(self.backref, True, resource_property=self)
