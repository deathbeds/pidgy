"""pidgy literate computing frame"""
from ._version import __version__

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
    shell.enable_html_pager = True

    shell.user_ns.setdefault("shell", shell)
    for e in ("tangle", "weave", "extras", "inspect", "magics"):
        shell.run_line_magic("load_ext", F"pidgy.{e}")


def unload_ipython_extension(shell):
    for e in ("tangle", "weave", "extras", "inspect", "magics"):
        shell.run_line_magic("unload_ext", F"pidgy.{e}")
