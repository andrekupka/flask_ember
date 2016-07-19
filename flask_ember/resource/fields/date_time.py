from sqlalchemy import types

from .data_field_base import DataFieldBase


class DateTime(DataFieldBase):
    __sql_type__ = types.DateTime
    __always_initialize_type__ = True
