---
---

# The `pidgy` extension for [Markdown][literate programming]

The pidgy implementation is successful because of the existing
shell configuration system provide by the [`IPython`].
[`IPython`] is an industry standard for interactive python programming,
and provided the substrate for the first [`IPython`] and later [`jupyter`]
notebook implementations. This unit specifically configurations the
high-level names we'll refer to when extending `pidgy` including the tangle and weave steps in literate computing.

<!--excerpt-->
<!--

    import jupyter, notebook, IPython, mistune as markdown, IPython as python, ast, jinja2 as template, importnb, doctest, pathlib
    with importnb.Notebook(lazy=True):
        try: from . import loader, tangle, extras
        except: import loader, tangle, extras
    with loader.pidgyLoader(lazy=True):
        try: from . import weave, testing, metadata
        except: import weave, testing, metadata

-->

There are two approaches to extending the `jupyter` experience:

1. Write custom jupyter extensions in python and javascript. (eg.[lab extensions], `IPython` widgets)
2. Use the existing configurable objects to modify behaviors in python. (eg. any jupyter kernel)

`pidgy` takes the second approach as it builds a [Markdown]-forward REPL interface. Frequently, the `load_ipython_extension` method reappears frequently in this work. This function is used by `IPython` to recognize modifications made by modules to the interactive shell. The `"load_ext reload_ext unload_ext"` line magics used commonly by other tools creating features for interactive computing. Demonstrated in the following, the `load_ipython_extension` recieves the current `IPython.InteractiveShell` as an argument to be configured.

    def load_ipython_extension(shell: IPython.InteractiveShell) -> None:

The `extension` module aggregates the extensions that were designed for `pidgy`.
Currently, `pidgy` defines 6 extensions to produce the enhanced literate programming experience. Each module configures isoluted components of the `IPython.InteractiveShell`.

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

[markdown]: #
[literate programming]: #
[`ipython`]: #
[`jupyter`]: #
[kernels]: https://github.com/jupyter/jupyter/wiki/Jupyter-kernels
[`ipython` extensions]: https://ipython.readthedocs.io/en/stable/config/extensions/
