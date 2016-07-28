from flask_ember.model.model_builder import ModelBuilder
from .resource_options import ResourceOptions
from .resource_preparation_builder import ResourcePreparationBuilder


class ResourceDescriptor:
    def __init__(self, resource):
        self.resource = resource
        self.resource_preparer = ResourcePreparationBuilder(resource)
        self.model_builder = ModelBuilder(resource)
        self.options = ResourceOptions(resource.__dict__.get('Meta', None))

        self.properties = dict()
        self.fields = dict()
        self.relationships = dict()

    def add_field(self, field, name):
        if name in self.properties:
            # TODO improve exception message
            raise Exception("Field '{}' already exists in resource "
                            "'{}'.".format(name, self.resource_name))
        self.properties[name] = field
        self.fields[name] = field
        self.model_builder.add_builder(field.get_builder())

    def add_relationship(self, relationship, name):
        if name in self.properties:
            # TODO improve exception message
            raise Exception("Relationship '{}' already exists in resource "
                            "'{}'.".format(name, self.resource_name))
        self.properties[name] = relationship
        self.relationships[name] = relationship
        self.model_builder.add_builder(relationship.get_builder())

    def get_property(self, name):
        return self.properties[name]

    def find_inverse_relationship(self, name, relationship):
        """ Determines the matching inverse relationship for the given
        relationship with the given property name.

        :param name: The property name of the given relationship.
        :type name: str
        :param relationship: The relationship for whom the inverse is to be
                             found.
        :type relationship: RelationshipBase
        :rtype: RelationshipBase
        """
        inverse = None
        for other in self.relationships.values():
            if relationship.is_inverse(other):
                if relationship.matching_backref_exists(other):
                    return other
                elif inverse is None:
                    inverse = other
                else:
                    assert False, ("There are multiple matching inverse "
                                   "relationships for relationship '{}' in "
                                   "resource '{}'. Please specify an inverse "
                                   "relationship explicitly with the "
                                   "'backref' parameter.".format(
                        name, self.resource_name))
        return inverse

    @property
    def resource_name(self):
        """ The name of the described resource.
        """
        return self.resource.__name__

    def __repr__(self):
        # TODO improve representation
        return str(self.__dict__)
