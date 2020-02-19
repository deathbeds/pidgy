The readme is the documentation and main application.

It should document and define the cli application and build steps.

# Derived applications of pidgin programs.

    
    import click, IPython, pidgy, nbconvert, pathlib
    Ø = __name__ == '__main__'
    if Ø:
        from graphviz import Source as 🕸
        import black as ⬛️, isort, mistune as markdown, runpy, IPython as python, nbformat, jsonschema as schema, nbconvert, notebook, __main__, nbconvert
        formats: set = {x.partition('_')[0] for x in nbconvert.get_export_names()}

    @click.group()
    def application()->None:
A successful `notebook` program could find uses outside of its
interactive state as programs, documentation, or tests.
`pidgy` programming includes a `click` command-line 
`application` to weave `notebook`s to other forms and tangle `notebook`s as source code.



    _CODE_FORMATS = "python script".split()

    class PythonExporter(nbconvert.exporters.PythonExporter):
        def from_notebook_node(self, nb, resources, **kw):
            str, resources = super().from_notebook_node(nb, resources, **kw)
            return black.format_str(isort.SortImports(
                file_contents=str
            ).output, mode=black.FileMode()), resources

    def document(to, files):
The `document` command is an opinionated wrapper that 
converts notebooks to formatted python programs
and readable documents.

        exporter = nbconvert.get_exporter(to)
It uses the `nbconvert` library that transforms the `nbformat` into other projections.

        if to in _CODE_FORMATS: 
`pidgy` introduces a new opinion to the notebook where
the input defines the output.
In literate programming terms, 
we tangle the input and weave the output.
The decoupling of the input & output means that proper
python code maybe extracted from the `input`.  `pidgy`
includes `⬛️ and isort` community conventions 
for formatting python to abide python styling guides.

            exporter = PythonExporter()
        else:
With `pidgy`, we may consider a cell output to be the intended
`display` set forth by an author.
A string opinion `pidgy` documents is that the `input`
is excluded from resulting document, where as typical
approaches view all code as essential or not essential.
            
            exporter = exporter(exclude_input=True)
        
        for file in files: ...
    
    

    
Add the `click` arguments outside of the cell so preserve vertical space.
    
    application.command()(
        click.option('-t', '--to', default='markdown')(
            click.argument('files', nargs=-1)(document)));

    @application.command(context_settings=dict(
        allow_extra_args=True,
    ))
    @click.argument('ref', type=click.STRING)
    @click.pass_context
    def run(ctx, ref):
The `document` function demonstrates that `pidgy` may 
export `python` code. 
    As a result the could be run as main scripts using the `runpy` modules.
        
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
                else:
                    __import__(ref)
            finally: sys.argv = argv

    @application.group()
    def kernel():
`pidgy` is mainly designed to improve the interactive experience
of creating literature in computational notebooks. 

    @kernel.command()
    def install(user=False, replace=None, prefix=None):
        manager = __import__('jupyter_client').kernelspec.KernelSpecManager()
        path = str((pathlib.Path(__file__).parent.parent / 'kernel' / 'spec').absolute())
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
        