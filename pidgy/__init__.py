with __import__("importnb").Notebook(lazy=True):
    try:
        from . import loader, tangle
        from .loader import pidgyLoader
    except:
        import loader, tangle
        from loader import pidgyLoader

with pidgyLoader(lazy=True):
    try:
        from . import weave, testing
    except:
        import weave, testing


def load_ipython_extension(shell):
    with loader.pidgyLoader(lazy=True):
        try:
            from .shell import load_ipython_extension, unload_ipython_extension
        except:
            from shell import load_ipython_extension, unload_ipython_extension

    load_ipython_extension(shell)


def unload_ipython_extension(shell):
    with loader.pidgyLoader(lazy=True):
        try:
            from .shell import load_ipython_extension, unload_ipython_extension
        except:
            from shell import load_ipython_extension, unload_ipython_extension

    unload_ipython_extension(shell)
