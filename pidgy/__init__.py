with __import__('importnb').Notebook(lazy=True):
    try: 
        from . import reuse
        from .reuse import pidgyLoader
    except: 
        import reuse
        from reuse import pidgyLoader

def load_ipython_extension(shell):
    with reuse.pidgyLoader(lazy=True):
        try: 
            from .extension import load_ipython_extension, unload_ipython_extension
        except: 
            from extension import load_ipython_extension, unload_ipython_extension
            
    load_ipython_extension(shell)

def unload_ipython_extension(shell): 
    with reuse.pidgyLoader(lazy=True):
            try: 
                from .extension import load_ipython_extension, unload_ipython_extension
            except: 
                from extension import load_ipython_extension, unload_ipython_extension

    unload_ipython_extension(shell)


def true():
    import IPython, pidgy.kernel.shell
    return isinstance(IPython.get_ipython(), pidgy.kernel.shell.pidgyShell)

def false(): return not true()

