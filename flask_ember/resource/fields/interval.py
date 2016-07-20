from sqlalchemy import types

from .field_base import FieldBase


class Interval(FieldBase):
    __sql_type__ = types.Interval
