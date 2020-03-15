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

    def export(files: typing.List[pathlib.Path], to:{'markdown', 'python'}='python', write:bool=False):
        export.convert(*files, to, write)

<!---->

    def test(ctx, files: list):

Formally test markdown documents, notebooks, and python files.

         import pytest
         pytest.main(ctx.args+['--doctest-modules', '--disable-pytest-warnings']+list(files))

<!---->

    application = autocli.autoclick(
        run, render, test, export, template,
        autocli.autoclick(
            kernel.install, kernel.uninstall, kernel.start, group=click.Group("kernel")
        ),
        context_settings=dict(allow_extra_args=True, ignore_unknown_options=True),
    )


    import pidgy, ast, pytest, builtins, types, runpy, importlib, inspect, pytest

    class CLILoader(pidgy.pidgyLoader):
        def visit(self, node):
            node = super().visit(node)
            self.body, self.annotations = ast.Module([]), ast.Module([])
            while node.body:
                element = node.body.pop(0)
                if isinstance(element, ast.AnnAssign) and element.target.id[0].islower():
                    try:
                        if element.value:
                            ast.literal_eval(element.value)
                        self.annotations.body.append(element)
                        continue
                    except: ...
                self.body.body.append(element)
            return self.body

[art of the readme]: https://github.com/noffle/art-of-readme
[readme history]: https://medium.com/@NSomar/readme-md-history-and-components-a365aff07f10
