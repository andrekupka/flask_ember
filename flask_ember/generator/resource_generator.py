from flask_ember.util.string import dasherize


class ResourceGenerator:

    def __init__(self, ember, resource_class):
        self.ember = ember
        self.resource_class = resource_class

    def generate(self, app):
        # TODO generation of api endpoints etc
        resource = self.resource_class
        name = resource.__qualname__
        print("Generated %s" % name)
        app.add_url_rule('/' + dasherize(name), name, lambda: name)
