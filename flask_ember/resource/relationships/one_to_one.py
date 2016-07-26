from flask_ember.model.relationship_builder import RelationshipBuilder
from .relationship_base import RelationshipBase


class OneToOne(RelationshipBase):
    def __init__(self, target_kind, backref):
        # TODO Fix the determination of the inverse side. Currently this is
        # done automatically if the inverse relationship is not defined
        # explicitly. Otherwise a foreign key will be generated on both sides
        # and sqlalchemy will fail. Also have a look at
        # create_inverse_relationship.
        super().__init__(target_kind, backref)

    def create_property_builder(self):
        return RelationshipBuilder(self.backref, use_list=False,
                                   resource_property=self)

    def get_inverse_class(self):
        return OneToOne
