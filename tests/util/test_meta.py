import unittest

from flask_ember.util.meta import (get_attributes, get_class_attributes,
                                   get_inherited_attributes)


class Parent:
    p = 1


class Intermediate(Parent):
    i = 2
    t = (1, 2)


class Child(Intermediate):
    c = 3


class MetaTestCase(unittest.TestCase):

    def is_int(self, name, attribute):
        return isinstance(attribute, int)

    def is_tuple(self, name, attribute):
        return isinstance(attribute, tuple)

    def test_get_class_attributes(self):
        attributes = get_class_attributes(Child, self.is_int)
        self.assert_attributes(attributes, ['c'], [Child.c])
        no_attributes = get_class_attributes(Child, self.is_tuple)
        self.assert_no_attributes(no_attributes)

    def test_get_attributes(self):
        attributes = get_attributes(Child, self.is_int)
        self.assert_attributes(attributes, ['p', 'i', 'c'], [Parent.p,
                                                             Intermediate.i,
                                                             Child.c])
        attributes = get_attributes(Child, self.is_tuple)
        self.assert_attributes(attributes, ['t'], [Intermediate.t])

    def test_get_inherited_attributes(self):
        attributes = get_inherited_attributes(Child, self.is_int)
        self.assert_attributes(attributes, ['p', 'i'], [Parent.p,
                                                        Intermediate.i])

    def assert_no_attributes(self, attributes):
        self.assertEqual(len(attributes), 0)

    def assert_attributes(self, attributes, expected_names,
                          expected_attributes):
        expectations = zip(expected_names, expected_attributes)
        self.assertEqual(attributes, list(expectations))
