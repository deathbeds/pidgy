from . import base, util, compat


with __import__("importnb").Notebook(lazy=True):
    try:
        from . import tangle, loader
    except:
        import tangle, loader
pidgyLoader = loader.pidgyLoader
with pidgyLoader(lazy=True):
    try:
        from . import weave, testing, magic, runpidgy
        from .extension import load_ipython_extension, unload_ipython_extension
    except:
        import weave, testing, magic, runpidgy
        from extension import load_ipython_extension, unload_ipython_extension

if __import__("IPython").get_ipython():
    magic.load_ipython_extension(__import__("IPython").get_ipython())
