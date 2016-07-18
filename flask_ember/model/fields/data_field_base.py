from .field_base import FieldBase


class DataFieldBase(FieldBase):
    SQL_TYPE = None

    def __init__(self, primary_key=False, column_options=None, **kwargs):
        merge_options = dict(primary_key=primary_key)
        if column_options:
            column_options.update(merge_options)
        else:
            column_options = merge_options
        super().__init__(column_options=column_options, **kwargs)

    def create_sql_type(self):
        return self.SQL_TYPE
