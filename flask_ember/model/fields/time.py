from sqlalchemy import types

from .data_field_base import DataFieldBase


class Time(DataFieldBase):
    __sql_type__ = types.Time
