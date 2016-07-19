from sqlalchemy import types

from .data_field_base import DataFieldBase


class Date(DataFieldBase):
    __sql_type__ = types.Date
    __dont_initialize_type__ = True
