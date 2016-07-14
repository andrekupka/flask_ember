from .generator import ResourceGenerator


class FlaskEmber:
    def __init__(self, app=None, db=None):
        self.resource_generators = list()

        if app and db:
            self.init_app(app, db)

    def init_app(self, app, db):
        app.ember = self
        app.model_base = db.Model

        self.generate_resources(app)

    def generate_resources(self, app):
        for generator in self.resource_generators:
            generator.generate(app, self)

    def resource(self, resource_class):
        generator = ResourceGenerator(resource_class)
        self.resource_generators.append(generator)
        return resource_class
