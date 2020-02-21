It should document and define the cli application and build steps.

# Derived applications of pidgin programs.

    import click, IPython, pidgy, nbconvert, pathlib
    _CODE_FORMATS = "python script".split()

    @click.group()
    def application()->None:

A successful `notebook` program could find uses outside of its interactive state
as programs, documentation, or tests. `pidgy` programming includes a `click`
command-line `application` to weave `notebook`s to other forms and tangle
`notebook`s as source code.

    @application.command(context_settings=dict(
        allow_extra_args=True,
    ))
    @click.argument('ref', type=click.STRING)
    @click.pass_context
    def run(ctx, ref):

The `document` function demonstrates that `pidgy` may export `python` code. As a
result the could be run as main scripts using the `runpy` modules.

        import pidgy, importnb, runpy, sys
        absolute = str(pathlib.Path().absolute())
        sys.path = ['.'] + sys.path
        with pidgy.pidgyLoader(main=True), importnb.Notebook(main=True):
            click.echo(F"Running {ref}.")
            sys.argv, argv = [ref] + ctx.args, sys.argv
            try:
                if pathlib.Path(ref).exists():
                    ref = ref.rstrip('.py').rstrip('.ipynb').rstrip('.md')
                if ref in sys.modules:
                    with pidgy.pidgyLoader(): # cant reload main
                        importlib.reload(__import__(ref))
                else: __import__(ref)
            finally: sys.argv = argv

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
