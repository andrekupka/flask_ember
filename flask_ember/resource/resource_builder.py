from abc import ABCMeta


class ResourceBuilder(metaclass=ABCMeta):

    def create_primary_key_columns(self):
        pass

    def create_non_primary_key_columns(self):
        pass

    def create_properties(self):
        pass
