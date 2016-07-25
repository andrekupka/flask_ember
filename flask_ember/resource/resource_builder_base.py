class ResourceBuilderBase:
    def __init__(self, resource):
        self.resource = resource
        self.finished = False

    @property
    def resource_name(self):
        return self.resource.__name__

    def is_finished(self):
        return self.finished

    def finalize(self):
        self.finished = True

    def execute_build_step(self, build_step):
        if not self.is_finished() and hasattr(self, build_step):
            getattr(self, build_step)()
