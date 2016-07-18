from .field_base import FieldBase


class DataFieldBase(FieldBase):
    SQL_TYPE = None

    def create_sql_type(self):
        return self.SQL_TYPE
