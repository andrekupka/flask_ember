from .relationship_base import RelationshipBase
from flask_ember.model.relationship_builder import RelationshipBuilder


class ManyToOne(RelationshipBase):

    def create_property_builder(self):
        return RelationshipBuilder(self.backref, False, resource_property=self)
