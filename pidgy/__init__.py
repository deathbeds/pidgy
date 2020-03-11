with __import__("importnb").Notebook(lazy=True):
    try:
        from . import loader
        from .loader import pidgyLoader
    except:
        import loader
        from loader import pidgyLoader

with pidgyLoader(lazy=True):
    try:
        from . import weave
        from .runpidgy import run
    except:
        import weave
        from runpidgy import run


def load_ipython_extension(shell):
    with loader.pidgyLoader(lazy=True):
        try:
            from .extension import load_ipython_extension, unload_ipython_extension
        except:
            from extension import load_ipython_extension, unload_ipython_extension

    load_ipython_extension(shell)


def unload_ipython_extension(shell):
    with loader.pidgyLoader(lazy=True):
        try:
            from .extension import load_ipython_extension, unload_ipython_extension
        except:
            from extension import load_ipython_extension, unload_ipython_extension

    unload_ipython_extension(shell)


def true():
    import IPython, pidgy.kernel.shell

    return isinstance(IPython.get_ipython(), pidgy.kernel.shell.pidgyShell)


def false():
    return not true()


import builtins

builtins.yes = builtins.true = True
builtins.no = builtins.false = False
builtins.null = None
