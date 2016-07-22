class ModelGenerator:

    def generate_models(self, resources):
        generation_methods = ['prepare_resource', 'create_table',
                              'create_primary_key_columns',
                              'create_non_primary_key_columns', 'setup_mapper',
                              'setup_properties', 'finalize']
        for method_name in generation_methods:
            for resource in resources:
                if not resource._model_generated:
                    resource._descriptor.call_model_builder(method_name)
