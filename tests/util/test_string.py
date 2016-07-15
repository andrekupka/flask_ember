import unittest

from flask_ember.util.string import (camelize, capitalize, classify, dasherize,
                                     decamelize, underscore)


class StringTestCase(unittest.TestCase):

    def test_camelize(self):
        values = ['innerHTML', 'action_name', 'css-class-name',
                  'my favorite items', 'My Favorite Items',
                  'private-docs/owner-invoice']
        expectations = ['innerHTML', 'actionName', 'cssClassName',
                        'myFavoriteItems', 'myFavoriteItems',
                        'privateDocs/ownerInvoice']
        self.assert_string_function(camelize, values, expectations)

    def test_capitalize(self):
        values = ['innerHTML', 'action_name', 'css-class-name',
                  'my favorite items', 'private-docs/owner-invoice']
        expectations = ['InnerHTML', 'Action_name', 'Css-class-name',
                        'My favorite items', 'Private-docs/Owner-invoice']
        self.assert_string_function(capitalize, values, expectations)

    def test_classify(self):
        values = ['innerHTML', 'action_name', 'css-class-name',
                  'my favorite items', 'private-docs/owner-invoice']
        expectations = ['InnerHTML', 'ActionName', 'CssClassName',
                        'MyFavoriteItems', 'PrivateDocs/OwnerInvoice']
        self.assert_string_function(classify, values, expectations)

    def test_dasherize(self):
        values = ['innerHTML', 'action_name', 'css-class-name',
                  'my favorite items', 'private-docs/owner-invoice']
        expectations = ['inner-html', 'action-name', 'css-class-name',
                        'my-favorite-items', 'private-docs/owner-invoice']
        self.assert_string_function(dasherize, values, expectations)

    def test_decamelize(self):
        values = ['innerHTML', 'action_name', 'css-class-name',
                  'my favorite items']
        expectations = ['inner_html', 'action_name', 'css-class-name',
                        'my favorite items']
        self.assert_string_function(decamelize, values, expectations)

    def test_underscore(self):
        values = ['innerHTML', 'action_name', 'css-class-name',
                  'my favorite items', 'private-docs/owner-invoice']
        expectations = ['inner_html', 'action_name', 'css_class_name',
                        'my_favorite_items', 'private_docs/owner_invoice']
        self.assert_string_function(underscore, values, expectations)

    def assert_string_function(self, function, values, expectations):
        for value, expectation in zip(values, expectations):
            self.assertEqual(function(value), expectation)
