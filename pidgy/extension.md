# `pidgy` extension

`pidgy` adds features to the `IPython` interactive shell using the extension configuration system.
Each `pidgy` modification is a module tailoring features for literate computing. In this stage we initialize the treatment of the tangle and weave steps of literate programming.

<!--excerpt-->

    import IPython, importnb
    def load_ipython_extension(shell: IPython.InteractiveShell) -> None:

The `extension` module aggregates the extensions that were designed for `pidgy`.
Currently, `pidgy` defines 6 extensions to produce the enhanced literate programming experience. Each module configures isoluted components of the `IPython.InteractiveShell`.

        with importnb.Notebook():
            try: from . import loader, tangle, extras
            except: import loader, tangle, extras
        with loader.pidgyLoader():
            try: from . import weave, testing, measure
            except: import weave, testing, measure
        loader.load_ipython_extension(shell)
        tangle.load_ipython_extension(shell)
        measure.load_ipython_extension(shell)
        extras.load_ipython_extension(shell)
        testing.load_ipython_extension(shell)
        weave.load_ipython_extension(shell)

`loader` ensures the ability to important python, markdown, and notebook documents
`tangle` defines the heuristics for translating [Markdown] to [Python].
`measure` retains information as the shell and kernel interact with each other.
`extras` introduces experimental syntaxes specific to `pidgy`.
`testing` adds unittest and doctest capabilities to each cell execution.
`weave` defines a [Markdown] forward display system that templates and displays the input.

<details><summary>What are the <code>load_ipython_extension and unload_ipython_extension</code></summary>{% filter markdown2html %}
`load_ipython_extension and unload_ipython_extension` are used by `IPython` to trigger modifications to the interactive shell by a module. These methods are inovked by the `"load_ext reload_ext unload_ext"` line magics. Demonstrated in the following, the `load_ipython_extension` recieves the current `IPython.InteractiveShell` as an argument to be configured.

    def unload_ipython_extension(shell):

`unload_ipython_extension` unloads all the extensions loads in `load_ipython_extension`.

        with importnb.Notebook():
            try: from . import loader, tangle, extras
            except: import loader, tangle, extras
        with loader.pidgyLoader():
            try: from . import weave, testing, metadata
            except: import weave, testing, metadata

        [x.unload_ipython_extension(shell) for x in (loader, weave, testing, extras, metadata, tangle)]

{% endfilter %}

</details>

[markdown]: #
[literate programming]: #
[ipython]: #
[`jupyter`]: #
[kernels]: https://github.com/jupyter/jupyter/wiki/Jupyter-kernels
[ipython extensions]: https://ipython.readthedocs.io/en/stable/config/extensions/
