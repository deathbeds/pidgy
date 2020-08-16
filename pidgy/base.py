import traitlets, IPython, sys


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
        
class Display(Trait):
    body = traitlets.Unicode(allow_none=True)
    vars = traitlets.Any()
    _display = traitlets.Any()

    def update(self, **kwargs):
        if self._display is None: return self.display(**kwargs)
        if 'nbval' in sys.modules: return 
        self._display.update(self.render(**kwargs))

    def render(self, **kwargs): 
        if self.body is not None:
            return self.displayer(self.body)

    def display(self, **kwargs):
        object = self.render(**kwargs)
        if object is None: return
        if self.vars:
            if self._display is None:
                self._display = IPython.display.display(object, display_id=True)
            else:
                self._display.display(object)
        else:
            IPython.display.display(object)

    _ipython_display_ = display

class MarkdownDisplay(Display):
    displayer = IPython.display.Markdown        
