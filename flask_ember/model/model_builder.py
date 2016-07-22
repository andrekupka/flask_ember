from sqlalchemy import Table
from sqlalchemy.orm import mapper
from sqlalchemy.sql import ColumnCollection

from flask_ember.resource.resource_property_base import ResourcePropertyBase


class ModelBuilder:

    def __init__(self, resource):
        self.resource = resource
        self.finished = False

        self.columns = ColumnCollection()
        self.constraints = list()
        self.properties = dict()

        self.has_primary_key = False
        self.has_primary_keys_done = False

        self.table = None
        self.mapper = None

        self.builders = list()

    # TODO where to parse options, extra model options class
    @property
    def options(self):
        return self.resource._descriptor.options

    @property
    def resource_name(self):
        return self.resource.__name__

    def add_builder(self, builder):
        self.builders.append(builder)

    def add_column(self, column):
        if column.key in self.columns:
            raise Exception("Duplicated column '{}' in resource '{}' is not "
                            "allowed".format(column.key, self.resource_name))
        self.columns.add(column)
        if column.primary_key:
            self.has_primary_key = True

        self.table.append_column(column)

    def add_constraint(self, constraint):
        # TODO check for duplicate constraint name?
        self.constraints.append(constraint)
        self.table.append_constraint(constraint)

    def add_property(self, name, prop):
        if name in self.properties:
            raise Exception("Duplicate property '{}' in resource '{}' is not "
                            "allowed".format(name))
        self.properties[name] = prop
        self.mapper.add_property(name, prop)

    def is_finished(self):
        return self.finished

    # setup phase methods

    def prepare_resource(self):
        to_delete = list()
        for name, attr in self.resource.__dict__.items():
            if isinstance(attr, ResourcePropertyBase):
                to_delete.append(name)
        for name in to_delete:
            delattr(self.resource, name)

    def create_table(self):
        tablename = self.options.get_tablename(self.resource_name)
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
        self.finished = True

    def _execute_builders(self, operation):
        for builder in self.builders:
            if hasattr(builder, operation):
                getattr(builder, operation)()

    def __repr__(self):
        # TODO improve representation
        return str(self.__dict__)
