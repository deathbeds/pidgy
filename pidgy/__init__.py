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


# do this in the kernel
import builtins

builtins.yes = builtins.true = True
builtins.no = builtins.false = False
builtins.null = None
