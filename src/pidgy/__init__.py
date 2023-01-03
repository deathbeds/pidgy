"""pidgy literate computing frame"""


IS_IPY = bool(
    getattr(
        __import__("sys").modules.get("IPython", __import__("sys")),
        "get_ipython",
        lambda: None,
    )()
)


def get_ipython():
    import IPython

    shell = IPython.get_ipython()
    if shell is None:
        shell = IPython.InteractiveShell()
        IPython.get_ipython = shell.get_ipython
    return shell


def get_cell_id(shell=None):
    return (shell or get_ipython()).kernel.get_parent().get("metadata", {}).get("cellId")


def load_ipython_extension(shell):
    from . import extras, pidgy, tangle, weave

    shell.user_ns.setdefault("shell", shell)

    tangle.load_ipython_extension(shell)
    weave.load_ipython_extension(shell)
    pidgy.load_ipython_extension(shell)
    extras.load_ipython_extension(shell)


def unload_ipython_extension(shell):
    from . import extras, pidgy, tangle, weave

    extras.unload_ipython_extension(shell)
    tangle.unload_ipython_extension(shell)
    pidgy.unload_ipython_extension(shell)
    weave.unload_ipython_extension(shell)
