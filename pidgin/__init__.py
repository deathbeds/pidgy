with __import__('importnb').Notebook(lazy=True):
    try: from . import imports
    except: import imports

with imports.PidginLoader(lazy=True):
    try: 
        from .extension import load_ipython_extension, unload_ipython_extension
    except: 
        from extension import load_ipython_extension, unload_ipython_extension

def true():
    import IPython, pidgin.kernel.shell
    return isinstance(IPython.get_ipython(), pidgin.kernel.shell.PidginShell)

def false(): return not true()