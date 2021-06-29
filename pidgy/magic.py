"""pidgy ipython magics


pidgy magics include: tangle, weave, parse, pidgy"""
import pprint

from . import get_ipython, parser, weave

LOADED = False


def weave(line, cell=None):
    import IPython
    return IPython.display.display(IPython.display.Markdown(cell or ""))


def tangle(line, cell=None):
    print(parser.Markdown().render(cell or ""))


def pidgy(line, cell=None):
    from . import LOADED, load_ipython_extension, unload_ipython_extension

    load_ipython_extension(get_ipython())
    try:

        result = get_ipython().run_cell(cell)

    finally:

        unload_ipython_extension(get_ipython())


def parse(line, cell=None):
    from . import parser

    pprint.pprint(parser.Markdown().parse(cell or ""))


def load_ipython_extension(shell):
    from . import kernel

    shell.register_magic_function(tangle, "cell")
    shell.register_magic_function(parse, "cell")
    shell.register_magic_function(weave, "cell")

    shell.register_magic_function(pidgy, "cell")


def unload_ipython_extension(shell):
    None
