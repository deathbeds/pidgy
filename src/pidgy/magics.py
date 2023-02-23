"""adds cell magic functions for pidgy.

the cell magics we use are:
* pidgy - allows running pidgy tangle and weave without a persistent extension
* weave - weaves the cell into interactive ipython displays
* tangle - tangles the cell into python


"""
from . import get_ipython, get_cell_id


def tangle(line, cell):
    """tangle the cell to python code."""
    from IPython.display import Code

    return Code(get_ipython().tangle.render(cell), language="python")


def parse(line, cell):
    """tangle the cell to python code."""
    return get_ipython().tangle.parse(cell)


def weave(line, cell):
    """weave the cell input into a display"""
    shell = get_ipython()

    from IPython.core.interactiveshell import ExecutionInfo, ExecutionResult
    return shell.weave.post_run_cell(ExecutionResult(ExecutionInfo(cell, True, False, True, get_cell_id())))


def pidgy(line, cell):
    """weave the cell input into a display"""
    shell = get_ipython()
    shell.run_cell(shell.tangle.render(cell), silent=True)
    return weave("", cell)


def load_ipython_extension(shell):
    from .tangle import _add_tangle_trait
    from .weave import _add_weave_trait, _add_interactivity

    _add_tangle_trait(shell)
    _add_weave_trait(shell)
    _add_interactivity(shell)


    shell.register_magic_function(tangle, "cell")
    shell.register_magic_function(parse, "cell")
    shell.register_magic_function(weave, "cell")
    shell.register_magic_function(pidgy, "cell")

def unload_ipython_extension(shell):
    from .weave import _rm_interactivity
    _rm_interactivity(shell)