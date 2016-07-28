from flask_ember.model.relationship_builder import RelationshipBuilder
from .relationship_base import RelationshipBase


class OneToOne(RelationshipBase):
    def __init__(self, target_kind, **kwargs):
        super().__init__(target_kind, **kwargs)

    def create_builder(self):
        return RelationshipBuilder(use_list=False, resource_property=self)

    def get_inverse_class(self):
        return OneToOne
