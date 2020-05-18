# Render and template output source

In literate programming, the input is representative of a published form. The original target for the WEB programming
implementation is the Device Independent Format used by Latex, and with the ability to target PDF. [Markdown] is
the `pidgy` document language. It is a plain text formatting syntax that has canonical representations in HTML.

An important feature of interactive computing in the browser is access to rich display object provided by
HTML and Javascript. `pidgy` takes advantage of the ability to include hypermedia forms that enhance and
support computational narratives.

    import dataclasses, IPython, pidgy

    @dataclasses.dataclass(unsafe_hash=True)
    class Weave:

        exporter = __import__('nbconvert').exporters.TemplateExporter()
        exporter.environment.loader.loaders.append(__import__('jinja2').FileSystemLoader('.'))

The `Weave` class controls the display of `pidgy` outputs.

        shell: object

        @pidgy.implementation
        def post_run_cell(self, result):

Show the woven output.

            text = pidgy.util.strip_front_matter(result.info.raw_cell)
            lines = text.splitlines() or ['']
            if not lines[0].strip(): return pidgy.util.html_comment(text)
            IPython.display.display(IPython.display.Markdown(self.render(text)))


        def render(self, text):
            import builtins, operator
            try:

Try to replace any jinja templates with information in the current namespace
and show the rendered view.

                template = self.exporter.environment.from_string(text, globals={
                    **vars(builtins), **vars(operator),
                    **(getattr(self.shell, 'user_ns', {})).get('__annotations__', {}),
                    **getattr(self.shell, 'user_ns', {})})
                text = template.render()
            except BaseException as Exception:
                IPython.get_ipython().showtraceback((type(Exception), Exception, Exception.__traceback__))

            return text
