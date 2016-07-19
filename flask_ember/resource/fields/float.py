from sqlalchemy import types

from .data_field_base import DataFieldBase


class Float(DataFieldBase):
    __sql_type__ = types.Float
    __always_initialize_type__ = True
