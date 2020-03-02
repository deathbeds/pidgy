# Weaving cells in pidgin programs

<!--

    import datetime, dataclasses, sys, IPython as python, IPython, nbconvert as export, collections, IPython as python, mistune as markdown, hashlib, functools, hashlib, jinja2.meta, pidgy
    exporter, shell = export.exporters.TemplateExporter(), python.get_ipython()
    modules = lambda:[x for x in sys.modules if '.' not in x and not str.startswith(x,'_')]
    with pidgy.pidgyLoader(lazy=True):
        try:
            from . import events
        except:
            import events


-->

pidgin programming is an incremental approach to documents.

    def load_ipython_extension(shell):
        shell.display_formatter.formatters['text/markdown'].for_type(str, lambda x: x)
        shell.weave = Weave(shell=shell)
        shell.weave.register()

    @dataclasses.dataclass
    class Weave(events.Events):
        shell: IPython.InteractiveShell = dataclasses.field(default_factory=IPython.get_ipython)
        environment: jinja2.Environment = dataclasses.field(default=exporter.environment)
        _null_environment = jinja2.Environment()

        def format_markdown(self, text):
            try:
                template = exporter.environment.from_string(text, globals=getattr(self.shell, 'user_ns', {}))
                text = template.render()
            except BaseException as Exception:
                self.shell.showtraceback((type(Exception), Exception, Exception.__traceback__))
            return text

        def format_metadata(self):
            parent = getattr(self.shell.kernel, '_last_parent', {})
            return {}

        def _update_filters(self):
            self.environment.filters.update({
                k: v for k, v in getattr(self.shell, 'user_ns', {}).items() if callable(v) and k not in self.environment.filters})


        def post_run_cell(self, result):
            text = strip_front_matter(result.info.raw_cell)
            lines = text.splitlines() or ['']
            IPython.display.display(IPython.display.Markdown(
                self.format_markdown(text) if lines[0].strip() else F"""<!--\n{text}\n\n-->""", metadata=self.format_metadata())
            )
            return result

    def unload_ipython_extension(shell):
        try:
            shell.weave.unregister()
        except:...

    def strip_front_matter(text):
        if text.startswith('---\n'):
            front_matter, sep, rest = text[4:].partition("\n---")
            if sep: return ''.join(rest.splitlines(True)[1:])
        return text
