# `pidgy` command line interface

> [**Eat Me, Drink Me, Read Me.**][readme history]

    import IPython, pidgy, pathlib, typing

    with pidgy.pidgyLoader():
        try: from . import kernel, autocli, runpidgy, util, export
        except: import kernel, autocli, runpidgy, util, export

<!--excerpt-->

<!---->

    def run(ctx, ref: str):

`pidgy` `run` makes it possible to execute `pidgy` documents as programs, and
view their pubished results.

        import pidgy, importnb, runpy, sys, importlib, jinja2, click
        absolute = str(pathlib.Path().absolute())
        sys.path = ['.'] + sys.path
        click.echo(F"Running {ref}.")
        sys.argv, argv = [ref] + ctx.args, sys.argv
        try:
            runpidgy.run(ref)
        finally: sys.argv = argv

    def render(ctx, ref: str):

        import pidgy, importnb, runpy, sys, importlib, jinja2, click
        absolute = str(pathlib.Path().absolute())
        sys.path = ['.'] + sys.path
        sys.argv, argv = [ref] + ctx.args, sys.argv
        try:
            click.echo(runpidgy.render(ref))

        finally: sys.argv = argv

    def export(files: typing.List[pathlib.Path], to:{'markdown', 'python'}='python', write:bool=False):
        export.convert(*files, to, write)

<!---->

    def test(ctx, files: list):

Formally test markdown documents, notebooks, and python files.

         import pytest
         pytest.main(ctx.args+['--doctest-modules', '--disable-pytest-warnings']+list(files))

<!---->

    application = autocli.autoclick(
        run, render, test, export,
        autocli.autoclick(
            kernel.install, kernel.uninstall, kernel.start, group=click.Group("kernel")
        ),
        context_settings=dict(allow_extra_args=True, ignore_unknown_options=True),
    )

[art of the readme]: https://github.com/noffle/art-of-readme
[readme history]: https://medium.com/@NSomar/readme-md-history-and-components-a365aff07f10
