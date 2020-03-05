---
---

# Configuring the [Markdown]-forward interactive shell in `IPython`

Open source software and practices shape the way `pidgy` is designed. It relies mainly on foundational tools from the scientific python computing community. The primary base for `pidgy` is the `IPython.InteractiveShell` that expose configurable features that customize the interactive computing experience. `IPython` is one of the heritage languages developed in into the award winning `jupyter` project.

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

Each module in `pidgy` is an `IPython` configuration module that transforms independent aspects of [Literate Computing]. Our extension appends the following abilities:

- `loader` ensures the ability to important python, markdown, and notebook documents as reusable modules.
- `tangle` defines the heuristics for translating [Markdown] to [Python].
- `extras` introduces experimental syntaxes specific to `pidgy`.
- `metadata` retains information as the shell and kernel interact with each other.
- `testing` adds unittest and doctest capabilities to each cell execution.
- `weave` defines a [Markdown] forward display system that templates and displays the input.

<details><summary>What are the <code>load_ipython_extension and unload_ipython_extension</code> </summary>
`load_ipython_extension and unload_ipython_extension` are used by `IPython` to trigger modifications to the interactive shell by a module. These methods are inovked by the `"load_ext reload_ext unload_ext"` line magics. Demonstrated in the following, the `load_ipython_extension` recieves the current `IPython.InteractiveShell` as an argument to be configured.
</details>

    def load_ipython_extension(shell: IPython.InteractiveShell) -> None:

The `extension` module aggregates the extensions that were designed for `pidgy`.
Currently, `pidgy` defines 6 extensions to produce the enhanced literate programming experience. Each module configures isoluted components of the `IPython.InteractiveShell`.

        [object.load_ipython_extension(shell) for object in (
            loader, tangle, extras, metadata, testing, weave
        )]
    ...

<!--

    def unload_ipython_extension(shell):

`unload_ipython_extension` unloads all the extensions loads in `load_ipython_extension`.

        [x.unload_ipython_extension(shell) for x in (loader, weave, testing, extras, metadata, tangle)]


-->

[markdown]: #
[literate programming]: #
[`ipython`]: #
[`jupyter`]: #
[kernels]: https://github.com/jupyter/jupyter/wiki/Jupyter-kernels
[`ipython` extensions]: https://ipython.readthedocs.io/en/stable/config/extensions/
