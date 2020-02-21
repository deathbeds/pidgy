It should document and define the cli application and build steps.

# Derived applications of pidgin programs.

    import click, IPython, pidgy, nbconvert, pathlib, re
    _CODE_FORMATS = "python script".split()

    @click.group()
    def application()->None:

A successful `notebook` program could find uses outside of its interactive state
as programs, documentation, or tests. `pidgy` programming includes a `click`
command-line `application` to weave `notebook`s to other forms and tangle
`notebook`s as source code.

    @application.command(context_settings=dict(allow_extra_args=True))
    @click.option('--verbose/--quiet', default=True)
    @click.argument('ref', type=click.STRING)
    @click.pass_context
    def run(ctx, ref, verbose):

The `document` function demonstrates that `pidgy` may export `python` code. As a
result the could be run as main scripts using the `runpy` modules.

        import pidgy, importnb, runpy, sys, importlib, jinja2
        comment = re.compile(r'(?s:<!--.*?-->)')
        absolute = str(pathlib.Path().absolute())
        sys.path = ['.'] + sys.path
        with pidgy.pidgyLoader(main=True), importnb.Notebook(main=True):
            click.echo(F"Running {ref}.")
            sys.argv, argv = [ref] + ctx.args, sys.argv
            try:
                if pathlib.Path(ref).exists():
                    for ext in ".py .ipynb .md".split():
                        if ref[-len(ext):] == ext:
                            ref = ref[:-len(ext)]
                if ref in sys.modules:
                    with pidgy.pidgyLoader(): # cant reload main
                        object = importlib.reload(importlib.import_module(ref))
                else: object = importlib.import_module(ref)
                if verbose:
                    if object.__file__.endswith('.md.ipynb'):
                        md = nbconvert.get_exporter('markdown')(exclude_output=True).from_filename(object.__file__)[0]
                    elif object.__file__.endswith('.ipynb'):
                        md = nbconvert.get_exporter('markdown')().from_filename(object.__file__)[0]
                    else:
                        md = pathlib.Path(object.__file__).read_text()
                    click.echo(
                        jinja2.Template(re.sub(comment, '', md)).render(vars(object)))
            finally: sys.argv = argv

    @application.command(context_settings=dict(allow_extra_args=True))
    @click.argument('file', nargs=-1, type=click.STRING)
    @click.pass_context
    def test(ctx, files):

Formally test markdown documents, notebooks, and python files.

         import pytest
         pytest.main(ctx.args+['--doctest-modules', '--disable-pytest-warnings']+files)

    @application.group()
    def kernel():

`pidgy` is mainly designed to improve the interactive experience of creating
literature in computational notebooks.

    @kernel.command()
    def install(user=False, replace=None, prefix=None):
        manager = __import__('jupyter_client').kernelspec.KernelSpecManager()
        path = str((pathlib.Path(__file__).parent / 'kernelspec').absolute())
        try:
            dest = manager.install_kernel_spec(path, 'pidgy')
        except:
            click.echo(F"System install was unsuccessful. Attempting to install the pidgy kernel to the user.")
            dest = manager.install_kernel_spec(path, 'pidgy', True)
        click.echo(F"The pidgy kernel was install in {dest}")

    @kernel.command()
    def uninstall(user=True, replace=None, prefix=None):
        __import__('jupyter_client').kernelspec.KernelSpecManager().remove_kernel_spec('pidgy')
        click.echo(F"The pidgy kernel was removed.")

    @kernel.command()
    @click.option('-f')
    def start(user=True, replace=None, prefix=None, f=None):
        import ipykernel.kernelapp
        with pidgy.pidgyLoader():
            from . import kernel
        ipykernel.kernelapp.IPKernelApp.launch_instance(
            kernel_class=kernel.pidgyKernel)
