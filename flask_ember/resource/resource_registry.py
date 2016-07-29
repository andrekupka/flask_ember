from collections import OrderedDict


class ResourceRegistry(OrderedDict):
    def resolve(self, target_kind):
        # TODO improve registry and resource resolution
        target = self.get(target_kind, None)
        assert target is not None, "Couldn't resolve target: '{}'".format(
            target_kind)
        return target
