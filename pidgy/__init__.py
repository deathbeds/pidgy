import pluggy

specification, implementation = (
    pluggy.HookspecMarker("pidgy"),
    pluggy.HookimplMarker("pidgy"),
)
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
        from .shell import load_ipython_extension, unload_ipython_extension
    except:
        import weave, testing
        from shell import load_ipython_extension, unload_ipython_extension
