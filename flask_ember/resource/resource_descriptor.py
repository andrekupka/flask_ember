from sqlalchemy import Table
from sqlalchemy.orm import mapper
from sqlalchemy.sql import ColumnCollection

from .resource_options import ResourceOptions
from .resource_property import ResourceProperty


class ResourceDescriptor:

    def __init__(self, resource):
        self.resource = resource
        self.options = ResourceOptions(getattr(resource, 'Meta', None))

        self.columns = ColumnCollection()

        self.has_primary_key = False

        self.builders = []

    def add_builder(self, builder):
        self.builders.append(builder)

    def add_column(self, column):
        if column.key in self.columns:
            raise Exception('Duplicated column {} is not '
                            'allowed'.format(column.key))
        self.columns.add(column)
        if column.primary_key:
            self.has_primary_key = True

    # setup phase methods

    def create_columns(self):
        self.execute_builders('create_columns')

    def setup_table(self):
        tablename = self.options.get_tablename(self.resource.__name__)
        table_args = list(self.columns)
        self.resource._table = Table(tablename, self.resource._metadata,
                                     *table_args)

    def setup_mapper(self):
        self.resource._mapper = mapper(self.resource, self.resource._table)

    def execute_builders(self, operation):
        for builder in self.builders:
            if hasattr(builder, operation):
                getattr(builder, operation)()

    def __repr__(self):
        # TODO improve representation
        return str(self.__dict__)
