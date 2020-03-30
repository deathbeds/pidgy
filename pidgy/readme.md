# `pidgy` command line interface

> [**Eat Me, Drink Me, Read Me.**][readme history]

    import IPython, pidgy, pathlib, typing, click, functools, contextlib, sys, types

    with pidgy.pidgyLoader():
        try: from . import kernel, autocli, runpidgy, util, export, weave
        except: import kernel, autocli, runpidgy, util, export, weave

<!--excerpt-->

    def run(ctx, ref: str):

`pidgy` `run` executes `pidgy` documents as programs.

        import pidgy, click
        click.echo(F"Running {ref}.")
        with pidgy.util.sys_path(), pidgy.util.argv(*([ref] + ctx.args)):
            runpidgy.run(ref)

    def template(ctx, ref: str, no_show:bool=False):

`pidgy` `template` executes `pidgy` documents as programs and publishes the templated results.

        import pidgy, click
        with pidgy.util.sys_path(), pidgy.util.argv(*([ref] + ctx.args)):
            data = pidgy.runpidgy.render(ref)
            if not no_show: click.echo(pidgy.util.ansify(data))

    def to(to:{'markdown', 'python'}, files: typing.List[pathlib.Path], write:bool=False):

Convert pidgy documents to other formats.

        pidgy.export.convert(*files, to=to, write=write)

<!---->

    def test(ctx, files: list):

Formally test markdown documents, notebooks, and python files.

         import pytest
         pytest.main(ctx.args+['--doctest-modules', '--disable-pytest-warnings']+list(files))

<!---->

    application = autocli.autoclick(
        run, test, to, template,
        autocli.autoclick(
            pidgy.kernel.install, pidgy.kernel.uninstall, pidgy.kernel.start, group=click.Group("kernel")
        ),
        context_settings=dict(allow_extra_args=True, ignore_unknown_options=True),
    )

[art of the readme]: https://github.com/noffle/art-of-readme
[readme history]: https://medium.com/@NSomar/readme-md-history-and-components-a365aff07f10
