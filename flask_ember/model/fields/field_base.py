from abc import ABCMeta


class FieldBase(metaclass=ABCMeta):

    def __init__(self, column_options=None):
        self.column_options = column_options or dict()
