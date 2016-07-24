from sqlalchemy import Column

from flask_ember.util.collections import merge_dicts
from .property_builder_base import PropertyBuilderBase


class FieldBuilder(PropertyBuilderBase):
    def __init__(self, sql_type, type_options, column_options, *args,
                 **kwargs):
        self.sql_type = sql_type
        self.type_options = type_options
        self.column_options = column_options
        super().__init__(*args, **kwargs)

    def override_type_options(self, extra_options):
        warning_message = ("Overriding already set type option '{{}}' with "
                           "'{{}}' for field '{}'.".format(self.name))
        merge_dicts(extra_options, self.type_options,
                    warning_message=warning_message)

    def override_column_options(self, extra_options):
        warning_message = ("Overriding already set column option '{{}}' with "
                           "'{{}}' for field '{}'.".format(self.name))
        merge_dicts(extra_options, self.column_options,
                    warning_message=warning_message)

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
