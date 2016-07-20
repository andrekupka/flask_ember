from sqlalchemy import types

from .field_base import FieldBase


class Time(FieldBase):
    __sql_type__ = types.Time
