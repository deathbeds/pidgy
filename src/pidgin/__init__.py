from ._version import *
with __import__('importnb').Notebook():  
    from .tangle import Pidgin
    from . import tangle

from .specifications import *

with Pidgin(): 
    from . import shell, weave
    from .shell import load_ipython_extension, unload_ipython_extension
    
from . import applications, specifications
from .applications import *

    
    
with PidginWeave(lazy=True): 
    from .docs import references

present = publishing.present