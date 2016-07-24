from flask_ember.model.relationship_builder import RelationshipBuilder
from .relationship_base import RelationshipBase


class OneToOne(RelationshipBase):
    def create_property_builder(self):
        return RelationshipBuilder(self.backref, False, False,
                                   resource_property=self)
