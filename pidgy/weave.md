# Weaving cells in pidgin programs

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
        def register(self, *, method=''):

A DRY method to `"register/unregister" kernel and shell extension objects.

            for event in self._events:
                callable = getattr(self, event, None)
                callable and getattr(self.shell.events, F'{method}register')(event, callable)

        unregister = functools.partialmethod(register, method='un')

    def load_ipython_extension(shell):
        shell.display_formatter.formatters['text/markdown'].for_type(str, lambda x: x)

Default to showing the markdown displays.

        shell.weave = Metadata(shell=shell)
        shell.weave.register()

    @dataclasses.dataclass
    class Metadata(Events):
        shell: IPython.InteractiveShell = dataclasses.field(default_factory=IPython.get_ipython)
        start: datetime.datetime = dataclasses.field(default_factory=datetime.datetime.utcnow().isoformat)
        modules: list = dataclasses.field(default_factory=list)
        ns: list = dataclasses.field(init=False)
        mapping: dict = dataclasses.field(default_factory=dict)
        environment: jinja2.Environment = dataclasses.field(default=exporter.environment)
        interactive: bool = True
        _null_environment = jinja2.Environment()
        variables: list = dataclasses.field(default_factory=dict)

        def pre_run_cell(self, info):
            cellId=self.shell.kernel._last_parent.get('metadata', {}).get('cellId', None)
            deletedCells=self.shell.kernel._last_parent.get('metadata', {}).get('deletedCells', [])
            self.shell.user_ns['CELL_MAPPING'] = self.shell.user_ns.get('CELL_MAPPING', self.mapping)
            self.mapping[cellId] = {'execution_count': self.shell.execution_count, 'started_at': self.shell.kernel._last_parent['header']['date']}
            for delete in deletedCells:
                if delete in self.mapping:
                    del self.mapping[delete]

            self.modules = modules()
            self.start = datetime.datetime.utcnow().isoformat()
            if hasattr(self.shell, 'user_ns'):
                self.ns = self.names()
            return info

        def names(self):
            return [x for x in self.shell.user_ns if x[0].islower()]

        def strip_front_matter(self, text):
            if text.startswith('---\n'):
                front_matter, sep, rest = text[4:].partition("\n---")
                if sep: return ''.join(rest.splitlines(True)[1:])
            return text

        def format_markdown(self, text):
            lines = text.splitlines() or ['']
            if lines[0].strip():
                exporter.environment.filters.update({
                    k: v for k, v in getattr(self.shell, 'user_ns', {}).items() if callable(v) and k not in exporter.environment.filters})
                try:
                    text = exporter.environment.from_string(text, globals=getattr(self.shell, 'user_ns', {})).render()
                except BaseException as Exception:
                    self.shell.showtraceback((type(Exception), Exception, Exception.__traceback__))
            return text

        def format_metadata(self):
            parent = getattr(self.shell.kernel, '_last_parent', {})
            return dict(
                    modules=[x for x in modules() if x not in self.modules],
                    names=[x for x in self.names() if x not in self.ns],
                    start_at=self.shell.kernel._last_parent['header']['date'].isoformat(),
                    end_at=datetime.datetime.utcnow().isoformat(),
                    sessionId=hashlib.sha256(str(self.shell).encode()).hexdigest(), #some uuid
                    cellId=parent.get('metadata', {}).get('cellId', None),
                    deletedCells=parent.get('metadata', {}).get('deletedCells', None)
                )

        def post_run_cell(self, result):
            text = self.strip_front_matter(result.info.raw_cell)
            lines = text.splitlines() or ['']
            if not lines[0].strip():
                IPython.display.display(F"""<!--\n{text}\n\n-->""")
            if lines[0].strip():
                metadata = self.format_metadata()
                self.mapping[metadata['cellId']]['input'] = result.info.raw_cell
                exporter.environment.filters.update({
                    k: v for k, v in getattr(self.shell, 'user_ns', {}).items() if callable(v) and k not in exporter.environment.filters})
                try:
                    template = exporter.environment.from_string(text, globals=getattr(self.shell, 'user_ns', {}))
                    text = template.render()
                except BaseException as Exception:
                    self.shell.showtraceback((type(Exception), Exception, Exception.__traceback__))
                variables = jinja2.meta.find_undeclared_variables(self._null_environment.parse(result.info.raw_cell))
                if variables and self.interactive:
                    self.mapping[metadata['cellId']]['display'] = IPython.display.display(IPython.display.Markdown(self.format_markdown(text), metadata=metadata), display_id=True)
                    self.mapping[metadata['cellId']]['variables'] = variables
                    updated = []
                    for variable in variables:
                        if variable not in self.variables:
                            self.variables[variable] = self.shell.user_ns.get(variable, None)


                else:
                    IPython.display.display(IPython.display.Markdown(self.format_markdown(text), metadata=metadata))

            variables = set(self.variables)
            for key, value in self.mapping.items():
                for variable in value.get('variables', []):
                    if self.variables[variable] is not self.shell.user_ns.get(variable, None):
                        self.variables[variable] = self.shell.user_ns[variable]
                        if 'display' in value:
                            try:
                                value['display'].update(IPython.display.Markdown(exporter.environment.from_string(value['input'], globals=getattr(self.shell, 'user_ns', {})).render()))
                            except: del value['display']
                        break

            return result

        def __post_init__(self):
            self.ns = [x for x in getattr(self.shell, 'user_ns', {}) if '.' not in x and not str.startswith(x,'_')]

    def unload_ipython_extension(shell):
        try:
            shell.weave.unregister()
        except:...
