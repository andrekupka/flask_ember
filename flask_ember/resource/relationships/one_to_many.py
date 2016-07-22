from .relationship_base import RelationshipBase
from flask_ember.model.relationship_builder import RelationshipBuilder


class OneToMany(RelationshipBase):

    def create_property_builder(self):
        return RelationshipBuilder(self.backref, True, resource_property=self)
