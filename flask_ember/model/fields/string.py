from sqlalchemy import types

from .data_field_base import DataFieldBase


class String(DataFieldBase):

    def __init__(self, length, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.length = length

    def create_sql_type(self):
        return types.String(self.length)
