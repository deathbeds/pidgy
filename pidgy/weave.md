# Weaving and template `pidgy`

<!--

    import dataclasses, IPython, nbconvert as convert, jinja2
    try: from . import base, util
    except: import base, util
    exporter = convert.exporters.TemplateExporter()

-->

pidgin programming is an incremental approach to documents.

    @dataclasses.dataclass
    class Weave(base.Extension):
        environment: jinja2.Environment = dataclasses.field(default=exporter.environment)

        def format_markdown(self, text):
            lines = text.splitlines() or ['']
            if not lines[0].strip(): return F"""<!--\n{text}\n\n-->"""
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
            text = util.strip_front_matter(result.info.raw_cell)
            IPython.display.display(IPython.display.Markdown(self.format_markdown(text), metadata=self.format_metadata()))
            return result

    def load_ipython_extension(shell):
        shell.weave = Weave(shell=shell)
        shell.weave.register()


    def unload_ipython_extension(shell):
        try:
            shell.weave.unregister()
        except:...
