from flask_ember.model.relationship_builder import RelationshipBuilder
from .relationship_base import RelationshipBase


class OneToOne(RelationshipBase):
    def __init__(self, target_kind, backref):
        super().__init__(target_kind, backref)

    def create_property_builder(self):
        return RelationshipBuilder(self.backref, use_list=False,
                                   resource_property=self)

    def get_inverse_class(self):
        return OneToOne
