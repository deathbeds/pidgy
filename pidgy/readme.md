# `pidgy` command line interface

> [**Eat Me, Drink Me, Read Me.**][readme history]

<!--excerpt-->

<!---->

    def run(ctx, ref: str):

`pidgy` `run` makes it possible to execute `pidgy` documents as programs, and
view their pubished results.

        import pidgy, importnb, runpy, sys, importlib, jinja2
        with pidgy.pidgyLoader():
            try: from . import runpidgy
            except: import runpidgy

        comment = re.compile(r'(?s:<!--.*?-->)')
        absolute = str(pathlib.Path().absolute())
        sys.path = ['.'] + sys.path
        click.echo(F"Running {ref}.")
        sys.argv, argv = [ref] + ctx.args, sys.argv
        try:
            runpidgy.run(ref)
        finally: sys.argv = argv

<!---->

    def test(ctx, files: list):

Formally test markdown documents, notebooks, and python files.

         import pytest
         pytest.main(ctx.args+['--doctest-modules', '--disable-pytest-warnings']+list(files))

<!---->

[art of the readme]: https://github.com/noffle/art-of-readme
[readme history]: https://medium.com/@NSomar/readme-md-history-and-components-a365aff07f10
