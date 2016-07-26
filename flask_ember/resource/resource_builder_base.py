class ResourceBuilderBase:
    def __init__(self, resource):
        self.resource = resource
        self.finalized = False

    @property
    def descriptor(self):
        return self.resource._descriptor

    @property
    def resource_name(self):
        return self.resource.__name__

    def finalize(self):
        self.finalized = True

    def execute_build_step(self, build_step):
        if not self.finalized and hasattr(self, build_step):
            getattr(self, build_step)()
