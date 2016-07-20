from sqlalchemy import types

from .field_base import FieldBase


class Date(FieldBase):
    __sql_type__ = types.Date
    __dont_initialize_type__ = True
