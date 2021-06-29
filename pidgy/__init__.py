"""pidgy literate computing frame"""

LOADED = False


def get_ipython():
    import IPython

    shell = IPython.get_ipython()
    if shell is None:
        shell = IPython.InteractiveShell()
        IPython.get_ipython = shell.get_ipython
    return shell


def load_ipython_extension(shell=None):
    global LOADED
    import sys

    shell = shell or get_ipython()

    # provide access to the shell from the namespace
    shell.user_ns.setdefault("shell", shell)
    parser.load_ipython_extension(shell)
    weave.load_ipython_extension(shell)
    kernel.load_ipython_extension(shell)
    magic.load_ipython_extension(shell)
    lisp.load_ipython_extension(shell)
    ast.load_ipython_extension(shell)
    testing.load_ipython_extension(shell)
    ns.load_ipython_extension(shell)
    emoji.load_ipython_extension(shell)

    if not LOADED:
        ns.pre_execute()
        import doctest
        import importlib

        importlib.reload(doctest)
    LOADED = True


def unload_ipython_extension(shell=None):
    shell = shell or get_ipython()
    parser.unload_ipython_extension(shell)
    weave.unload_ipython_extension(shell)
    kernel.unload_ipython_extension(shell)
    lisp.unload_ipython_extension(shell)
    ast.unload_ipython_extension(shell)
    testing.unload_ipython_extension(shell)
    ns.unload_ipython_extension(shell)
    emoji.unload_ipython_extension(shell)


from . import (ast, emoji, kernel, lisp, loader, magic, ns, parser, testing,
               weave)
