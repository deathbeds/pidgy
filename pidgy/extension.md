# The `pidgy` extension for programming in Markdown

The pidgy implementation is successful because of the existing
configuration system provide by the `IPython` shell & kernel.
`IPython` is an industry standard for interactive python programming,
and provided the substrate for the first `IPython` and later `jupyter`
notebook implementations.

There are two approaches to extending the `jupyter` experience:

1. Write custom jupyter extensions in python and javascript.
2. Use the existing configurable objects to modify behaviors in python.

`pidgy` takes the second approach as it builds a [Markdown]-forward REPL interface.

<!--

    import jupyter, notebook, IPython, mistune as markdown, IPython as python, ast, jinja2 as template, importnb, doctest, pathlib
    with importnb.Notebook(lazy=True):
        try: from . import loader, tangle, extras
        except: import loader, tangle, extras
    with loader.pidgyLoader(lazy=True):
        try: from . import weave, testing, metadata
        except: import weave, testing, metadata
-->

> The `load_ipython_extension` method reappears frequently in this work. This function
> is used by `IPython` to recognize modifications to the interactive shell.

    def load_ipython_extension(shell: IPython.InteractiveShell) -> None:

The `extension` module aggregates the extensions that were designed for `pidgy`.
Currently, `pidgy` defines 6 extensions to produce the enhanced literate programming experience..

        [object.load_ipython_extension(shell) for object in (
            loader, tangle, extras, metadata, testing, weave
        )]
    ...

- `loader` ensures the ability to important python, markdown, and notebook documents as reusable modules.
- `tangle` defines the heuristics for translating [Markdown] to [Python].
- `extras` introduces experimental syntaxes specific to `pidgy`.
- `metadata` retains information as the shell and kernel interact with each other.
- `testing` adds unittest and doctest capabilities to each cell execution.
- `weave` defines a [Markdown] forward display system that templates and displays the input.

<!--

    def unload_ipython_extension(shell):

`unload_ipython_extension` unloads all the extensions loads in `load_ipython_extension`.

        for x in (weave, testing, extras, metadata, tangle):
            x.unload_ipython_extension(shell)

-->
