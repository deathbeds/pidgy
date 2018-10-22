with __import__('importnb').Notebook():
    from . import base
    from . import _doctest
    from . import _graphviz
    from . import _matplotlib
    from . import _pidgin
    from . import phrases
    from . import embed
    from . import flexlist
    
modules = _doctest, _graphviz, base, _matplotlib, flexlist, embed, phrases, _pidgin

def load_ipython_extension(ip):
    for module in modules:
        getattr(module, 'load_ipython_extension', lambda x: x)(ip)

def unload_ipython_extension(ip):
    for module in modules:
        getattr(module, 'unload_ipython_extension', lambda x: x)(ip)
