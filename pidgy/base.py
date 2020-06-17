import traitlets

class Trait(traitlets.HasTraits):
    parent = traitlets.Any()
    register_keys = "pre_execute pre_run_cell post_run_cell post_execute".split()
    def register(self):
        for key in self.register_keys:
            if hasattr(self, key):
                self.parent.events.register(key, getattr(self, key))