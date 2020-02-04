with __import__('importnb').Notebook(lazy=True):
    try: from . import reuse, __style__
    except: import reuse, __style__

pidgyLoader = reuse.pidgyLoader

with pidgyLoader(lazy=True):
    try: 
        from .extension import load_ipython_extension, unload_ipython_extension
    except: 
        from extension import load_ipython_extension, unload_ipython_extension

def true():
    import IPython, pidgy.kernel.shell
    return isinstance(IPython.get_ipython(), pidgy.kernel.shell.pidgyShell)

def false(): return not true()

