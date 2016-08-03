from flask_ember.model.one_to_one_relationship_builder import \
    OneToOneRelationshipBuilder
from .one_sided_relationship_base import OneSidedRelationshipBase


class OneToOne(OneSidedRelationshipBase):
    def create_builder(self):
        return OneToOneRelationshipBuilder(resource_property=self)

    def get_inverse_class(self):
        return OneToOne

    def configure_inverse(self, inverse):
        if self.primary is None:
            self.primary = True
        inverse.primary = not self.primary
        super().configure_inverse(inverse)
