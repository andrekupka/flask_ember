from .integer import Integer


class Id(Integer):
    def __init__(self, **kwargs):
        super().__init__(primary_key=True, **kwargs)
