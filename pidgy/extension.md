# The interactive `pidgy` interface

`pidgy` documents are written in interactive programming environments that make
it easy to run code and preview outputs. This specific implementation is bound
to the `IPython` kernel to be used in `jupyter` `notebook` and `jupyterlab`.

<!--

    import jupyter, notebook, IPython, mistune as markdown, IPython as python, ast, jinja2 as template, importnb as _import_, doctest, pathlib
    with _import_.Notebook(lazy=True):
        try: from . import reuse, translate
        except: import reuse, translate
    with reuse.pidgyLoader(lazy=True):
        try: from . import outputs, testing
        except: import outputs, testing
-->

    def load_ipython_extension(shell: IPython.InteractiveShell) -> None:

The `load_ipython_extension and unload_ipython_extension` are functions that can
configure the `IPython.InteractiveShell`. We'll introduce a few major features
that are configured everytime `pidgy` is used interactively.

1.  Configure the ability to import other `pidgy` markdown files and notebooks
    as python modules.  
    reuse.load_ipython_extension(shell)

2.  Perhaps the most labourious part of `pidgy` are the heuristics for a
    line-by-line translation of markdown source to python.

            translate.load_ipython_extension(shell)

3)  `pidgy` documents will frequently sprinkle `"code"` throughout a document.
    It uses this code as interactive test objects that are run as unit tests.

            testing.load_ipython_extension(shell)

4.  The `pidgy` `input` represents both code and design. We trigger a few custom
    output events to capture reproducible information about the computing
    environment.  
    outputs.load_ipython_extension(shell)

<!--

    def unload_ipython_extension(shell):
        for x in (outputs, testing, translate):
            x.unload_ipython_extension(shell)

-->