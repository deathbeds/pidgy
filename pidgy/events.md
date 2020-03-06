# The `IPython` [Read-Eval-Print-Loop]

> 44. Sometimes I think the only universal in the computing field is the fetch-execute cycle.
>     > Alan Perlis - Perlisisms

The [Read-Eval-Print-Loop] is a familiar interface to execute code and programs run by a compiler. The `IPython` project orginally began as an terminal application that was designed to improve the interactive experience when working [Python]. Eventually, `IPython` moved outside the terminal and into the browser with `IPython` `notebook`s that allowed authors that capture the process of their computational thinking supplemented with supporting hypermedia.

<!--excerpt-->

`IPython` exposes a few configurable states during a [Read-Eval-Print-Loop], `pidgy` modifies each state as an `IPython` extension. What follows is an explanation of what the heuristics `IPython` when executing code.

<!--

    import datetime, dataclasses, sys, IPython as python, IPython, nbconvert as export, collections, IPython as python, mistune as markdown, hashlib, functools, hashlib, jinja2.meta, ast
    exporter, shell = export.exporters.TemplateExporter(), python.get_ipython()
    modules = lambda:[x for x in sys.modules if '.' not in x and not str.startswith(x,'_')]

-->

    @dataclasses.dataclass
    class Events:

The `Events` is used for all the `pidgy` extensions to simplify registering and unregistering `IPython` extensions.

        _events = "pre_execute pre_run_cell post_execute post_run_cell".split()
        shell: IPython.InteractiveShell = dataclasses.field(default_factory=IPython.get_ipython)

        def register(self, shell=None, *, method=''):

`Events.register`s the object as an `IPython` extension, it mimics the interface for the `load_ipython_extension` and `unload_ipython_extension` methods.

            shell = shell or self.shell
            for event in self._events:
                callable = getattr(self, event, None)
                callable and getattr(shell.events, F'{method}register')(event, callable)
            if isinstance(self, ast.NodeTransformer):
                if method:

`ast.NodeTransformers` can be used to intercept parsed [Python] code and apply changes before compilations. If the `Events` object
is an `ast.NodeTransfromer` then it is registered on the current shell.

                    shell.ast_transformers.pop(shell.ast_transformers.index(self))
                else:
                    shell.ast_transformers.append(self)

            return self

        unregister = functools.partialmethod(register, method='un')

[read-eval-print-loop]: #
[perlisisms]: https://www.cs.yale.edu/homes/perlis-alan/quotes.html
