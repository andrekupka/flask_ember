import flask_ember.resource.relationships
from flask_ember.model.one_to_many_relationship_builder import \
    OneToManyRelationshipBuilder
from .one_sided_relationship_base import OneSidedRelationshipBase


class OneToMany(OneSidedRelationshipBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, primary=True, **kwargs)

    def create_builder(self):
        return OneToManyRelationshipBuilder(use_list=True,
                                            resource_property=self)

    def get_inverse_class(self):
        return flask_ember.resource.relationships.ManyToOne
