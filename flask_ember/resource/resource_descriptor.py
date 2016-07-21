from sqlalchemy import Table
from sqlalchemy.orm import mapper
from sqlalchemy.sql import ColumnCollection

from .resource_options import ResourceOptions


class ResourceDescriptor:

    def __init__(self, resource):
        self.resource = resource
        self.options = ResourceOptions(resource.__dict__.get('Meta', None))

        self.columns = ColumnCollection()
        self.constraints = list()
        self.properties = dict()

        self.relationships = dict()

        self.has_primary_key = False
        self.has_primary_keys_done = False

        self.builders = list()

    def add_builder(self, builder):
        self.builders.append(builder)

    def add_column(self, column):
        if column.key in self.columns:
            raise Exception('Duplicated column {} is not '
                            'allowed'.format(column.key))
        self.columns.add(column)
        if column.primary_key:
            self.has_primary_key = True

        self.table.append_column(column)

    def add_constraint(self, constraint):
        self.constraints.append(constraint)
        self.table.append_constraint(constraint)

    def add_relationship(self, name, relationship):
        if name in self.relationships:
            raise Exception('Duplicated relationship {} is not '
                            'allowed'.format(name))
        self.relationships[name] = relationship

    def add_property(self, name, prop):
        if name in self.properties:
            raise Exception('Duplicate property {} is not '
                            'allowed'.format(name))
        self.properties[name] = prop
        self.mapper.add_property(name, prop)

    def find_relationship(self, name):
        # TODO retrieve relationships from parent
        return self.relationships.get(name)

    # setup phase methods

    def create_table(self):
        tablename = self.options.get_tablename(self.resource.__name__)
        self.table = Table(tablename, self.resource._metadata)
        self.resource._table = self.table

    def create_primary_key_columns(self):
        # If the primary keys have already been generated indirectly by a
        # related class abort.
        if self.has_primary_keys_done:
            return

        self._execute_builders('create_primary_key_columns')
        self.has_primary_keys_done = True

    def create_non_primary_key_columns(self):
        self._execute_builders('create_non_primary_key_columns')

    def setup_mapper(self):
        self.mapper = mapper(self.resource, self.resource._table)
        self.resource._mapper = self.mapper

    def setup_properties(self):
        self._execute_builders('create_properties')

    def finalize(self):
        self.resource._setup_done = True

    def _execute_builders(self, operation):
        for builder in self.builders:
            if hasattr(builder, operation):
                getattr(builder, operation)()

    def __repr__(self):
        # TODO improve representation
        return str(self.__dict__)
