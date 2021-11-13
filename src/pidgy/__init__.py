"""__init__.py"""

"""pidgy literate computing frame"""

LOADED = False


def get_ipython():
    import IPython

    shell = IPython.get_ipython()
    if shell is None:
        shell = IPython.InteractiveShell()
        IPython.get_ipython = shell.get_ipython
    return shell


def load_ipython_extension(shell):
    from . import tangle, weave

    shell.user_ns.setdefault("shell", shell)
    tangle.load_ipython_extension(shell)
    weave.load_ipython_extension(shell)


def unload_ipython_extension(shell):
    from . import tangle, weave

    tangle.unload_ipython_extension(shell)
    weave.unload_ipython_extension(shell)
