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
    """pidgy is an enriched IPython interactive shell.

    it starts from a basic interactive shell and is configured by
    loading traits and extensions."""
    global LOADED

    shell = shell or get_ipython()

    # provide access to the shell from the namespace
    shell.user_ns.setdefault("shell", shell)

    # make markdown our primary input language by
    # adding our parser to the input transformation
    # this is where we introduce tangle to our cells
    parser.load_ipython_extension(shell)

    # modify our display to display our markdown
    # and make it interactive when configured.
    weave.load_ipython_extension(shell)

    # add our tangle and weave methods as magics that we can use
    magic.load_ipython_extension(shell)

    # install testing as part of the weave process for our cells
    testing.load_ipython_extension(shell)

    # support of emoji and completion
    emoji.load_ipython_extension(shell)

    if not LOADED:
        import doctest
        import importlib

        # some weird ipython conflict happens and we nee dto reload doctest
        importlib.reload(doctest)
    LOADED = True


def unload_ipython_extension(shell=None):
    shell = shell or get_ipython()
    parser.unload_ipython_extension(shell)
    weave.unload_ipython_extension(shell)
    testing.unload_ipython_extension(shell)

    emoji.unload_ipython_extension(shell)


from . import emoji, magic, parser, testing, weave
