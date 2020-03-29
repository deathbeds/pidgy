import pluggy

specification, implementation = (
    pluggy.HookspecMarker("pidgy"),
    pluggy.HookimplMarker("pidgy"),
)
with __import__("importnb").Notebook(lazy=True):
    try:
        from . import loader, tangle, extras
        from .loader import pidgyLoader
    except:
        import loader, tangle, extras
        from loader import pidgyLoader

with pidgyLoader(lazy=True):
    try:
        from . import weave, testing, magic, runpidgy
        from .shell import load_ipython_extension, unload_ipython_extension
    except:
        import weave, testing, magic, runpidgy
        from shell import load_ipython_extension, unload_ipython_extension

if __import__("IPython").get_ipython():
    magic.load_ipython_extension(__import__("IPython").get_ipython())
