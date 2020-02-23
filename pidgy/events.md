# Events along the `IPython` execution process.

<!--

    import datetime, dataclasses, sys, IPython as python, IPython, nbconvert as export, collections, IPython as python, mistune as markdown, hashlib, functools, hashlib, jinja2.meta
    exporter, shell = export.exporters.TemplateExporter(), python.get_ipython()
    modules = lambda:[x for x in sys.modules if '.' not in x and not str.startswith(x,'_')]

-->

This is your wysiwyg

pidgin programming is an incremental approach to documents.

    @dataclasses.dataclass
    class Events:

The `Events` class is a configurable `dataclasses` object that simplifies
configuring code execution and metadata collection during interactive computing
sessions.

        shell: IPython.InteractiveShell = dataclasses.field(default_factory=IPython.get_ipython)
        _events = "pre_execute pre_run_cell post_execute post_run_cell".split()
        def register(self, shell=None, *, method=''):
            shell = shell or self.shell

A DRY method to `"register/unregister" kernel and shell extension objects.

            for event in self._events:
                callable = getattr(self, event, None)
                callable and getattr(shell.events, F'{method}register')(event, callable)

        unregister = functools.partialmethod(register, method='un')
