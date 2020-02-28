# The `IPython` step during a [Read-Eval-Print-Loop] iteration.

> 44. Sometimes I think the only universal in the computing field is the fetch-execute cycle.
>     >

During a fetch-execute cycle in interactive computing, a [Read-Eval-Print-Loop] (ie. REPL) application transmits input to a compiler that returns a representative display for the source. `IPython` is [Read-Eval-Print-Loop] application for interactive python programming. It is a product of the scientific computing that
required the ability interact with code to gain insight about information.

`IPython` is superset of [Python], it provides custom syntaxes (eg. magics, system calls). `IPython` designed a configurable interface that can customize the input source before executing a command.

<!--

    import datetime, dataclasses, sys, IPython as python, IPython, nbconvert as export, collections, IPython as python, mistune as markdown, hashlib, functools, hashlib, jinja2.meta, ast
    exporter, shell = export.exporters.TemplateExporter(), python.get_ipython()
    modules = lambda:[x for x in sys.modules if '.' not in x and not str.startswith(x,'_')]

-->

    @dataclasses.dataclass
    class Events:

The `Events` class is a configurable `dataclasses` object that simplifies
configuring code execution and metadata collection during interactive computing
sessions.
There are a few note-worthy events that `IPython` identifies.

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

self.shell.ast_transformers.pop(self.shell.ast_transformers.index(self))
else:
self.shell.ast_transformers.append(self)

return self

<!--

        unregister = functools.partialmethod(register, method='un')

-->

[read-eval-print-loop]: #
[perlisisms]: https://www.cs.yale.edu/homes/perlis-alan/quotes.html
