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
        for inverse_name, inverse in self.relationships.items():
            # TODO match target types
            if relationship.match_other(inverse) and relationship.backref == \
                    inverse_name and inverse.backref == name:
                return inverse
        return None

    @property
    def resource_name(self):
        """ Returns the name of the described resource.

        :rtype: str
        """
        return self.resource.__name__

    def __repr__(self):
        # TODO improve representation
        return str(self.__dict__)
