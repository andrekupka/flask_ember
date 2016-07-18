from sqlalchemy import types

from .data_field_base import DataFieldBase


class String(DataFieldBase):
    __sql_type__ = types.String

    def __init__(self, length, *args, **kwargs):
        self.set_type_options(kwargs, length=length)
        super().__init__(*args, **kwargs)
