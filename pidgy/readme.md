# `"readme.md"` is a good name for a file.

> [**Eat Me, Drink Me, Read Me.**][readme history]

In `pidgy`, the `"readme.md"` is treated as the description and implementation
of the `__main__` program. The code below outlines the `pidgy` command line
application to reuse literate `pidgy` documents in `markdown` and `notebook`
files. It outlines how static `pidgy` documents may be reused outside of the
interactive context.

<!--excerpt-->

    ...

The functions are:

- Install the `pidgy` kernel.

```bash
pidgy kernel
```

- Run `pidgy` documents.

```bash
pidgy run
```

- Test `pidgy` documents.

```bash
pidgy test
```

- Exporting `pidgy` documents.

```bash
pidgy export
```

<!--

    import click, IPython, pidgy, nbconvert, pathlib, re

-->

    @click.group()
    def application()->None:

The `pidgy` `application` will group together a few commands that can view,
execute, and test pidgy documents.

<!---->

    @application.command(context_settings=dict(allow_extra_args=True))
    @click.option('--verbose/--quiet', default=True)
    @click.argument('ref', type=click.STRING)
    @click.pass_context
    def run(ctx, ref, verbose):

`pidgy` `run` makes it possible to execute `pidgy` documents as programs, and
view their pubished results.

        import pidgy, importnb, runpy, sys, importlib, jinja2
        comment = re.compile(r'(?s:<!--.*?-->)')
        absolute = str(pathlib.Path().absolute())
        sys.path = ['.'] + sys.path
        with pidgy.pidgyLoader(main=True), importnb.Notebook(main=True):
            click.echo(F"Running {ref}.")
            sys.argv, argv = [ref] + ctx.args, sys.argv
            try:
                if pathlib.Path(ref).exists():
                    for ext in ".py .ipynb .md".split(): ref = ref[:-len(ext)] if ref[-len(ext):] == ext else ref
                if ref in sys.modules:
                    with pidgy.pidgyLoader(): # cant reload main
                        object = importlib.reload(importlib.import_module(ref))
                else: object = importlib.import_module(ref)
                if verbose:
                    md = (nbconvert.get_exporter('markdown')(
                        exclude_output=object.__file__.endswith('.md.ipynb')).from_filename(object.__file__)[0]
                            if object.__file__.endswith('.ipynb')
                            else pathlib.Path(object.__file__).read_text())
                    md = re.sub(comment, '', md)
                    click.echo(
                        jinja2.Template(md).render(vars(object)))
            finally: sys.argv = argv

<!---->

    @application.command(context_settings=dict(allow_extra_args=True))
    @click.argument('files', nargs=-1, type=click.STRING)
    @click.pass_context
    def test(ctx, files):

Formally test markdown documents, notebooks, and python files.

         import pytest
         pytest.main(ctx.args+['--doctest-modules', '--disable-pytest-warnings']+list(files))

<!---->

    @application.group()
    def kernel():

`pidgy` is mainly designed to improve the interactive experience of creating
literature in computational notebooks.

<!---->

    @kernel.command()
    def install(user=False, replace=None, prefix=None):

`install` the pidgy kernel.

        manager = __import__('jupyter_client').kernelspec.KernelSpecManager()
        path = str((pathlib.Path(__file__).parent / 'kernelspec').absolute())
        try:
            dest = manager.install_kernel_spec(path, 'pidgy')
        except:
            click.echo(F"System install was unsuccessful. Attempting to install the pidgy kernel to the user.")
            dest = manager.install_kernel_spec(path, 'pidgy', True)
        click.echo(F"The pidgy kernel was install in {dest}")

<!---->

    @kernel.command()
    def uninstall(user=True, replace=None, prefix=None):

`uninstall` the kernel.

        import jupyter_client
        jupyter_client.kernelspec.KernelSpecManager().remove_kernel_spec('pidgy')
        click.echo(F"The pidgy kernel was removed.")

<!---->

    @kernel.command()
    @click.option('-f')
    def start(user=True, replace=None, prefix=None, f=None):

Launch a `pidgy` kernel applications.

        import ipykernel.kernelapp
        with pidgy.pidgyLoader():
            from . import kernel
        ipykernel.kernelapp.IPKernelApp.launch_instance(
            kernel_class=kernel.pidgyKernel)

<!---->

[art of the readme]: https://github.com/noffle/art-of-readme
[readme history]:
  https://medium.com/@NSomar/readme-md-history-and-components-a365aff07f10
