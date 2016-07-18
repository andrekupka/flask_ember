from sqlalchemy import types

from .data_field_base import DataFieldBase


class Interval(DataFieldBase):
    __sql_type__ = types.Interval
    __always_initialize_type__ = True
