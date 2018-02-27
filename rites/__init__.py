from .rites import load_ipython_extension, unload_ipython_extension 
load_ipython_extension()

from . import markdown, template, testing
from .widgets import manager