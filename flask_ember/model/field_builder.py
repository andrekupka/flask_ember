from sqlalchemy import Column

from .property_builder_base import PropertyBuilderBase


class FieldBuilder(PropertyBuilderBase):

    def __init__(self, sql_type, type_options, column_options, *args,
                 **kwargs):
        self.sql_type = sql_type
        self.type_options = type_options
        self.column_options = column_options
        super().__init__(*args, **kwargs)

    def create_primary_key_columns(self):
        self.create_column(True)

    def create_non_primary_key_columns(self):
        self.create_column(False)

    def create_column(self, primary_key):
        # TODO incorporate the column_name option, therefore override the
        # register_with_descriptor method and add a property
        if self.column_options.get('primary_key', False) == primary_key:
            used_type = self.sql_type(**self.type_options)
            column = Column(self.name, used_type, **self.column_options)
            self.add_table_column(column)
