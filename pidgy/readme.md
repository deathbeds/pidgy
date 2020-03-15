# `pidgy` command line interface

> [**Eat Me, Drink Me, Read Me.**][readme history]

    import IPython, pidgy, pathlib, typing, click, functools, contextlib, sys, types

    with pidgy.pidgyLoader():
        try: from . import kernel, autocli, runpidgy, util, export, weave
        except: import kernel, autocli, runpidgy, util, export, weave

<!--excerpt-->

<!---->

    @contextlib.contextmanager
    def sys_path():
        root = '.' in sys.path
        if root:
            sys.path = ['.'] + sys.path
        yield
        if root:
            sys.path.pop(sys.path.index('.'))

    def run(ctx, ref: str):

`pidgy` `run` makes it possible to execute `pidgy` documents as programs, and view their pubished results.

        import pidgy, click
        click.echo(F"Running {ref}.")
        with sys_path(), pidgy.util.argv(*([ref] + ctx.args)):
            runpidgy.run(ref)

    def render(ctx, ref: str):

        import pidgy, click
        with sys_path(), pidgy.util.argv(*([ref] + ctx.args)):
            click.echo(runpidgy.render(ref))

    def template(ctx, ref: str, no_show:bool=False):
        import pidgy, click
        with sys_path(), pidgy.util.argv(*([ref] + ctx.args)):
            data = runpidgy.parameterize(ref)
            if not no_show: click.echo(runpidgy.format_output(data))

    def to(to:{'markdown', 'python'}, files: typing.List[pathlib.Path], write:bool=False):
        export.convert(*files, to=to, write=write)

<!---->

    def test(ctx, files: list):

Formally test markdown documents, notebooks, and python files.

         import pytest
         pytest.main(ctx.args+['--doctest-modules', '--disable-pytest-warnings']+list(files))

<!---->

    application = autocli.autoclick(
        run, render, test, to, template,
        autocli.autoclick(
            kernel.install, kernel.uninstall, kernel.start, group=click.Group("kernel")
        ),
        context_settings=dict(allow_extra_args=True, ignore_unknown_options=True),
    )

[art of the readme]: https://github.com/noffle/art-of-readme
[readme history]: https://medium.com/@NSomar/readme-md-history-and-components-a365aff07f10
