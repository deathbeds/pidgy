from . import tangle, weave


def load_ipython_extension(shell):
    tangle.load_ipython_extension(shell)
    weave.load_ipython_extension(shell)


def unload_ipython_extension(shell):
    tangle.unload_ipython_extension(shell)
    weave.unload_ipython_extension(shell)
