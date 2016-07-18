from abc import ABCMeta, abstractmethod


class FieldBase(metaclass=ABCMeta):

    def __init__(self, column_options=None):
        self.column_options = column_options or dict()

    @abstractmethod
    def create_sql_type(self):
        pass
