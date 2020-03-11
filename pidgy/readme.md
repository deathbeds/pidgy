# `pidgy` command line interface

> [**Eat Me, Drink Me, Read Me.**][readme history]

    import click, IPython, pidgy, nbconvert, pathlib, re
    with pidgy.pidgyLoader():
        try: from . import kernel, autocli, runpidgy
        except: import kernel, autocli, runpidgy

<!--excerpt-->

<!---->

## `"pidgy run"` literature as code

    def run(ctx, ref: str):

`pidgy` `run` makes it possible to execute `pidgy` documents as programs, and
view their pubished results.

        import pidgy, importnb, runpy, sys, importlib, jinja2
        comment = re.compile(r'(?s:<!--.*?-->)')
        absolute = str(pathlib.Path().absolute())
        sys.path = ['.'] + sys.path
        click.echo(F"Running {ref}.")
        sys.argv, argv = [ref] + ctx.args, sys.argv
        try:
            runpidgy.run(ref)
        finally: sys.argv = argv

<!---->

## Test `pidgy` documents in pytest.

    def test(ctx, files: list):

Formally test markdown documents, notebooks, and python files.

         import pytest
         pytest.main(ctx.args+['--doctest-modules', '--disable-pytest-warnings']+list(files))

<!---->

    application = autocli.autoclick(run, test, kernel.application)

[art of the readme]: https://github.com/noffle/art-of-readme
[readme history]: https://medium.com/@NSomar/readme-md-history-and-components-a365aff07f10
