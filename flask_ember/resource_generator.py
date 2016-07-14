class ResourceGenerator:
    def __init__(self, resource_class):
        self.resource_class = resource_class

    def generate(self, app, ember):
        resource = self.resource_class
        name = resource._options.route or resource.__name__
        print(name)
        print(resource._options)
        app.add_url_rule('/' + name, name, lambda x=name: x)
