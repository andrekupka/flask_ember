import flask_ember.resource.relationships
from flask_ember.model.many_to_one_relationship_builder import \
    ManyToOneRelationshipBuilder
from .one_sided_relationship_base import OneSidedRelationshipBase


class ManyToOne(OneSidedRelationshipBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, primary=False, **kwargs)

    def create_builder(self):
        return ManyToOneRelationshipBuilder(use_list=False,
                                            resource_property=self)

    def get_inverse_class(self):
        return flask_ember.resource.relationships.OneToMany
