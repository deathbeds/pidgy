from .rites import load_ipython_extension, unload_ipython_extension 
load_ipython_extension()

from . import markdown, template, testing
import sys
from functools import partial
from ipywidgets import VBox, HBox, Text, Button

__all__ = 'manager',

class Updating(VBox):
    def _handle_displayed(self, **dict):
        global manager, EXTENSIONS
        for module, load, unload in (
            (module, getattr(module, 'load_ipython_extension'), getattr(module, 'unload_ipython_extension', None))
            for module in sys.modules.values() if hasattr(module, 'load_ipython_extension')
        ):
            def empty(callable, *object): return callable(__import__('IPython').get_ipython())
            if module not in EXTENSIONS:
                box = HBox(children=(
                    Text(value=getattr(module, '__module__', getattr(module, '__name__'))), Button(description='load'),
                ))
                box.children[1].on_click(partial(empty, load))
                if unload:
                    box.children += Button(description='unload'),
                    box.children[2].on_click(partial(empty, unload))
                EXTENSIONS += module, 
                manager.children += box, 
        super(VBox, self)._handle_displayed(**dict)

manager = Updating()
EXTENSIONS = tuple()
