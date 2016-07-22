from abc import ABCMeta


class PropertyBuilderBase(metaclass=ABCMeta):

    def __init__(self, resource_property):
        self.resource_property = resource_property

    @property
    def name(self):
        return self.resource_property.name

    @property
    def resource(self):
        return self.resource_property.resource

    @property
    def table(self):
        return self.resource._table

    @property
    def builder(self):
        return self.resource._descriptor.get_model_builder()

    def add_table_column(self, column):
        self.builder.add_column(column)

    def add_mapper_property(self, name, prop):
        self.builder.add_property(name, prop)

    def create_primary_key_columns(self):
        pass

    def create_non_primary_key_columns(self):
        pass

    def create_properties(self):
        pass
