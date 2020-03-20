# Render and template output source

In literate programming, the input is representative of a published form. The original target for the WEB programming
implementation is the Device Independent Format used by Latex, and with the ability to target PDF. [Markdown] is
the `pidgy` document language. It is a plain text formatting syntax that has canonical representations in HTML.

An important feature of interactive computing in the browser is access to rich display object provided by
HTML and Javascript. `pidgy` takes advantage of the ability to include hypermedia forms that enhance and
support computational narratives.

    import dataclasses, IPython, nbconvert as convert, jinja2, pidgy, builtins, sys, operator
    exporter = convert.exporters.TemplateExporter() # leave an global exporter avai

    try:
        from . import util
    except:
        import util

The `Weave` class controls the display of `pidgy` outputs.

    def post_run_cell(result):

Show the woven output.

        text = util.strip_front_matter(result.info.raw_cell)
        IPython.display.display(IPython.display.Markdown(format_markdown(text)))

    def format_markdown(text):
            lines = text.splitlines() or ['']
            if not lines[0].strip(): return F"""<!--\n{text}\n\n-->"""
            try:

Try to replace any jinja templates with information in the current namespace
and show the rendered view.

                template = exporter.environment.from_string(text, globals={
                    **vars(builtins), **vars(operator),
                    **getattr(IPython.get_ipython(), 'user_ns', {})
                })
                text = template.render()
            except BaseException as Exception:
                IPython.get_ipython().showtraceback((type(Exception), Exception, Exception.__traceback__))
            return text
