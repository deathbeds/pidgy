from dataclasses import dataclass, field
from midgy import Python
from . import get_ipython
def wrap_magic(function, cell_key="cell"):
    import functools
    import shlex

    import click
    import typer

    app = typer.Typer(
        add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}
    )
    app.command()(function)
    ctx = click.Context(typer.main.get_command(app))

    @functools.wraps(function)
    def magic(line, cell=None):
        try:
            ctx.command.parse_args(ctx, shlex.split(line))
        except click.exceptions.Exit:
            return
        if cell_key in ctx.params:
            ctx.params[cell_key] = cell
        return function(**ctx.params)

    magic.__doc__ = "\n".join((function.__doc__ or "", get_help(ctx)))
    return magic


def register_magic(function, name=None, cell_key="cell"):
    import inspect

    from . import get_ipython

    shell = get_ipython()
    cache_rich_console()
    signature = inspect.signature(function)
    wrapper = wrap_magic(function, cell_key=cell_key)
    kind = "line"
    if cell_key in signature.parameters:
        kind = "line_cell"
        if signature.parameters[cell_key].default is inspect._empty:
            kind = "cell"
    shell.register_magic_function(wrapper, kind, name)
    shell.log.info(f"registered {repr(function)} as magic named {name or function.__name__}")
    return function


def cache_rich_console(cache={}):
    import functools

    import typer

    if not cache:
        cache.setdefault("_get_rich_console", typer.rich_utils._get_rich_console)
    typer.rich_utils._get_rich_console = functools.lru_cache(cache["_get_rich_console"])


def get_help(ctx):
    import typer

    with typer.rich_utils._get_rich_console().capture() as console:
        ctx.get_help()
    return console.get()


def parse(**kwargs):
    cell = kwargs.pop("cell")
    shell = get_ipython()
    return type(shell.tangle)(**kwargs).parse(cell)

def tangle(**kwargs):
    cell = kwargs.pop("cell")
    shell = get_ipython()
    return type(shell.tangle)(**kwargs).parse(cell)


def weave(**kwargs):
    cell = kwargs.pop("cell")
    shell = get_ipython()
    return type(shell.tangle)(**kwargs).parse(cell)

def pidgy(**kwargs):
    return

def set_signature():
    pass


def load_ipython_extension(shell):
    shell.tangle
    pass