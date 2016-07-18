from sqlalchemy import types

from .data_field_base import DataFieldBase


class Integer(DataFieldBase):
    SQL_TYPE = types.Integer
