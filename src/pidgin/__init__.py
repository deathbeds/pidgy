from ._version import *
with __import__('importnb').Notebook():  
    from .tangle import Pidgin
    from . import tangle

from .specification import *

with Pidgin(): 
    from . import shell, weave, formatter
    from .shell import load_ipython_extension, unload_ipython_extension
    
from . import application, specification
from .application import *
from .specification import *

with Pidgin():
    from .application import pytest_
    
from .shell import load_ipython_extension, unload_ipython_extension

present = publishing.present