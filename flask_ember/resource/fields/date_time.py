from sqlalchemy import types

from .field_base import FieldBase


class DateTime(FieldBase):
    __sql_type__ = types.DateTime
    __always_initialize_type__ = True
