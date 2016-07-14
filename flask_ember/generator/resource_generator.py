from flask_ember.util.string import dasherize

class ResourceGenerator:
    def __init__(self, resource_class):
        self.resource_class = resource_class

    def generate(self, app, ember):
        # TODO generation of model, api etc
        resource = self.resource_class
        name = resource._options.route or resource.__name__
        app.add_url_rule('/' + dasherize(name), name, lambda x=name: x)
