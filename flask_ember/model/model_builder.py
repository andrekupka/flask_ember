from sqlalchemy import Table
from sqlalchemy.orm import mapper
from sqlalchemy.sql import ColumnCollection

from flask_ember.resource.resource_builder_base import ResourceBuilderBase
from flask_ember.resource.resource_property_base import ResourcePropertyBase


class ModelBuilder(ResourceBuilderBase):
    BUILD_STEPS = ['prepare_resource', 'create_table',
                   'create_primary_key_columns',
                   'create_non_primary_key_columns', 'setup_mapper',
                   'setup_properties', 'finalize']

    def __init__(self, resource):
        self.columns = ColumnCollection()
        self.constraints = list()
        self.properties = dict()

        self.has_primary_key = False
        self.has_primary_keys_done = False

        self.table = None
        self.mapper = None

        self.builders = list()

        super().__init__(resource)

    # TODO where to parse options, extra model options class
    @property
    def options(self):
        return self.descriptor.options

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

    # build phase methods

    def prepare_resource(self):
        to_delete = list()
        for name, attr in self.resource.__dict__.items():
            if isinstance(attr, ResourcePropertyBase):
                to_delete.append(name)
        for name in to_delete:
            delattr(self.resource, name)

    def create_table(self):
        tablename = self.options.get_table_name(self.resource_name)
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

    def _execute_builders(self, operation):
        for builder in self.builders:
            if hasattr(builder, operation):
                getattr(builder, operation)()

    def __repr__(self):
        # TODO improve representation
        return str(self.__dict__)

    @staticmethod
    def execute_build_steps(resources):
        get_builder = lambda res: res._descriptor.model_builder
        model_builders = list(map(get_builder, resources))
        for build_step in ModelBuilder.BUILD_STEPS:
            for builder in model_builders:
                builder.execute_build_step(build_step)
