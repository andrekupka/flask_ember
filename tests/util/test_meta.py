import inspect
import unittest


from flask_ember.util.meta import get_fields, get_class_fields, get_methods


class Parent:
    pfield = 1

    def pmethod(self):
        pass


class Intermediate(Parent):
    ifield = 2
    tfield = (1, 2)

    def imethod(self):
        pass


class Child(Intermediate):
    cfield = 3

    def cmethod(self):
        pass


class MetaTestCase(unittest.TestCase):

    def is_int(self, name, field):
        return isinstance(field, int)

    def is_tuple(self, name, field):
        return isinstance(field, tuple)

    def test_get_class_fields(self):
        fields = get_class_fields(Child, self.is_int)
        self.assert_fields(fields, ['cfield'], [Child.cfield])
        no_fields = get_class_fields(Child, self.is_tuple)
        self.assert_no_fields(no_fields)

    def test_get_fields(self):
        fields = get_fields(Child, self.is_int)
        self.assert_fields(fields, ['pfield', 'ifield', 'cfield'],
                           [Parent.pfield, Intermediate.ifield, Child.cfield])
        fields = get_fields(Child, self.is_tuple)
        self.assert_fields(fields, ['tfield'], [Intermediate.tfield])

    def test_get_methods(self):
        methods = get_methods(Child)
        self.assert_fields(methods, ['pmethod', 'imethod', 'cmethod'],
                           [Parent.pmethod, Intermediate.imethod,
                            Child.cmethod])

    def assert_no_fields(self, fields):
        self.assertEqual(len(fields), 0)

    def assert_fields(self, fields, expected_names, expected_fields):
        expectations = zip(expected_names, expected_fields)
        self.assertEqual(fields, list(expectations))
