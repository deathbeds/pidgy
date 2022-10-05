"""pidgy literate computing frame"""


IS_IPY = bool(
    getattr(
        __import__("sys").modules.get("IPython", __import__("sys")),
        "get_ipython",
        lambda: None,
    )()
)


def load_ipython_extension(shell):
    from . import extras, tangle, weave

    shell.user_ns.setdefault("shell", shell)

    extras.load_ipython_extension(shell)
    tangle.load_ipython_extension(shell)
    weave.load_ipython_extension(shell)


def unload_ipython_extension(shell):
    from . import extras, tangle, weave

    extras.unload_ipython_extension(shell)
    tangle.unload_ipython_extension(shell)
    weave.unload_ipython_extension(shell)
