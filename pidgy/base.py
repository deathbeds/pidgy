import traitlets


class Trait(traitlets.HasTraits):
    parent = traitlets.Any()
    enabled = traitlets.Bool(True)
    register_keys = "pre_execute pre_run_cell post_run_cell post_execute".split()

    def register(self):
        for key in self.register_keys:
            if hasattr(self, key):
                self.parent.events.register(key, getattr(self, key))

    def toggle(self, object: bool):
        self.enabled = bool(object if object is None else not self.enabled)
