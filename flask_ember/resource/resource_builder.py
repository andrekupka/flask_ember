from abc import ABCMeta


class ResourceBuilder(metaclass=ABCMeta):

    def create_columns(self):
        pass

    def add_table_column(self, column):
        self.resource._descriptor.add_column(column)
