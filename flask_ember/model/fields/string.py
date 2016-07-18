from sqlalchemy import types

from .data_field_base import DataFieldBase


class String(DataFieldBase):
    __sql_type__ = types.String

    def __init__(self, length=None, *args, **kwargs):
        self.add_sql_options(kwargs, length=length)
        super().__init__(*args, **kwargs)
