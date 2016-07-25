from flask_ember.model.model_builder import ModelBuilder


class ModelGenerator:
    def generate_models(self, resources):
        for build_step in ModelBuilder.BUILD_STEPS:
            for resource in resources:
                descriptor = resource._descriptor
                if not descriptor.is_model_generated():
                    descriptor.call_model_builder(build_step)
