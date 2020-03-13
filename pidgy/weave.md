# Render and template output source

In literate programming, the input is representative of a published form. The original target for the WEB programming
implementation is the Device Independent Format used by Latex, and with the ability to target PDF. [Markdown] is
the `pidgy` document language. It is a plain text formatting syntax that has canonical representations in HTML.

An important feature of interactive computing in the browser is access to rich display object provided by
HTML and Javascript. `pidgy` takes advantage of the ability to include hypermedia forms that enhance and
support computational narratives.

    import dataclasses, IPython, nbconvert as convert, jinja2
    try: from . import base, util
    except: import base, util
    exporter = convert.exporters.TemplateExporter() # leave an global exporter avai

The `Weave` class controls the display of `pidgy` outputs.

    @dataclasses.dataclass
    class Weave(base.Extension):
        def post_run_cell(self, result):
            text = util.strip_front_matter(result.info.raw_cell)
            IPython.display.display(IPython.display.Markdown(self.format_markdown(text), metadata=self.format_metadata()))
            return result

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



    def load_ipython_extension(shell): shell.weave = Weave(shell=shell).register()

    def unload_ipython_extension(shell):
        if hasattr(shell, 'weave'): shell.weave.unregister()

Albeit our approach does not specifically target `".DVI"` files, they are produced by ReadTheDocs when creating a PDF
from Latex.
