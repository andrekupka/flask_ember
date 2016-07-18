from abc import ABCMeta


class FieldBase(metaclass=ABCMeta):

    def __init__(self, type_options=None, column_options=None):
        self.type_options = type_options or dict()
        self.column_options = column_options or dict()
