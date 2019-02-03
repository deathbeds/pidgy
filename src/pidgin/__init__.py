from ._version import *
with __import__('importnb').Notebook():  from . import tangle
Pidgin = tangle.Pidgin

with Pidgin(lazy=True): 
    from .pidgin import *
    from . import weave, inspector, pidgin as _pidgin, docs, publishing, testing
    
present = publishing.present
    