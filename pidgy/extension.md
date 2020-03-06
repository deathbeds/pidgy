# Configuring the [Markdown]-forward interactive shell in `IPython`

This sections registers and describes each of the extensions that `pidgy` applies to the interactive shell.
The implementations of the extension are shaped by existing open source software and practices, and run throughout all aspects of the `pidgy` project. Specifically, this work relies on tooling from the scientific [Python] community.

<!--excerpt-->

`IPython` is a keystone application in the scientific python computing system and is one of the heritage langauges that evolved in the award winning `jupyter` project. The `ipykernel and IPython` are configurable [Python] objects that prescribe how code is executed while interactive computing. The `pidgy` extension is a collection of individual documents that configure individual components of the [Read-Eval-Print-Loop] application.

    import IPython, importnb

Each module in `pidgy` is an `IPython` configuration module that transforms independent aspects of [Literate Computing].

<details><summary>What are the <code>load_ipython_extension and unload_ipython_extension</code> </summary>
`load_ipython_extension and unload_ipython_extension` are used by `IPython` to trigger modifications to the interactive shell by a module. These methods are inovked by the `"load_ext reload_ext unload_ext"` line magics. Demonstrated in the following, the `load_ipython_extension` recieves the current `IPython.InteractiveShell` as an argument to be configured.
</details>

    def load_ipython_extension(shell: IPython.InteractiveShell) -> None:

The `extension` module aggregates the extensions that were designed for `pidgy`.
Currently, `pidgy` defines 6 extensions to produce the enhanced literate programming experience. Each module configures isoluted components of the `IPython.InteractiveShell`.

        with importnb.Notebook():
            try: from . import loader, tangle, extras
            except: import loader, tangle, extras
        with loader.pidgyLoader():
            try: from . import weave, testing, metadata
            except: import weave, testing, metadata
        ...

- `loader` ensures the ability to important python, markdown, and notebook documents
- `tangle` defines the heuristics for translating [Markdown] to [Python].
- `extras` introduces experimental syntaxes specific to `pidgy`.
- `metadata` retains information as the shell and kernel interact with each other.
- `testing` adds unittest and doctest capabilities to each cell execution.
- `weave` defines a [Markdown] forward display system that templates and displays the input.

        loader.load_ipython_extension(shell)
        tangle.load_ipython_extension(shell)
        metadata.load_ipython_extension(shell)
        extras.load_ipython_extension(shell)
        testing.load_ipython_extension(shell)
        weave.load_ipython_extension(shell)


    def unload_ipython_extension(shell):

`unload_ipython_extension` unloads all the extensions loads in `load_ipython_extension`.

        with importnb.Notebook():
            try: from . import loader, tangle, extras
            except: import loader, tangle, extras
        with loader.pidgyLoader():
            try: from . import weave, testing, metadata
            except: import weave, testing, metadata

        [x.unload_ipython_extension(shell) for x in (loader, weave, testing, extras, metadata, tangle)]

[markdown]: #
[literate programming]: #
[`ipython`]: #
[`jupyter`]: #
[kernels]: https://github.com/jupyter/jupyter/wiki/Jupyter-kernels
[`ipython` extensions]: https://ipython.readthedocs.io/en/stable/config/extensions/
