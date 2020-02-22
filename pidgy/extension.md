# The `pidgy` extension for programming in Markdown

The `IPython.InteractiveShell` has a configuration system for changing how
`"code"` interacts with the read-eval-print-loop (ie. REPL). `pidgy` uses this
system to provide a `markdown`-forward REPL interface that can be used with
`jupyter` tools.

<!--

    import jupyter, notebook, IPython, mistune as markdown, IPython as python, ast, jinja2 as template, importnb, doctest, pathlib
    with importnb.Notebook(lazy=True):
        try: from . import loader, tangle
        except: import loader, tangle
    with loader.pidgyLoader(lazy=True):
        try: from . import weave, testing
        except: import weave, testing
-->

    def load_ipython_extension(shell: IPython.InteractiveShell) -> None:

The `load_ipython_extension` makes it possible to configure and extend the
`IPython.InteractiveShell`.

        loader.load_ipython_extension(shell)
        tangle.load_ipython_extension(shell)
        testing.load_ipython_extension(shell)
        weave.load_ipython_extension(shell)
    ...

1. The `loader` makes it possible to import other markdown documents and
   notebooks as we would with any other [Python] module. The rub is that
   the source code in the program must **Restart and Run All**.
2. The `tangle` module constructes a line-for-line transformer that
   converts markdown to python.
3. `pidgy` documents can be used as unit tests. To assist in successful
   tests `pidgy` includes interactive `testing` with each execution. It
   verifies inline code, doctests, test functions, and
   `unittest.TestCase`s.
4. The `weave` step relies on the `IPython` rich display to show markdown.
   And `jinja` templates.

<!--

    def unload_ipython_extension(shell):

`unload_ipython_extension` unloads all the extensions loads in `load_ipython_extension`.

        for x in (weave, testing, tangle):
            x.unload_ipython_extension(shell)

-->
