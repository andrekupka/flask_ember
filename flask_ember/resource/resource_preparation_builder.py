from .resource_builder_base import ResourceBuilderBase


class ResourcePreparationBuilder(ResourceBuilderBase):
    BUILD_STEPS = ['prepare_relationships', 'finalize']

    def prepare_relationships(self):
        # The size of the relationship dictionary may change as
        # self-referential inverse relationships might be created.
        for relationship in list(self.descriptor.relationships.values()):
            relationship.resolve_inverse_relationships()

    @staticmethod
    def execute_build_steps(resources):
        get_preparer = lambda res: res._descriptor.resource_preparer
        preparers = list(map(get_preparer, resources))
        for build_step in ResourcePreparationBuilder.BUILD_STEPS:
            for preparer in preparers:
                preparer.execute_build_step(build_step)
