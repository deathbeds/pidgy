"jinja2 filters that make writing pidgy more fun"

from . import get_ipython
def q(q, cite):
    """<q>uotes"""
    return f"""<q cite="{cite}">{q}</q>"""

def i(id, height=600, width="100%"):
    """a filter for <q>uotes"""
    from urllib.parse import urlparse
    from html import escape

    parse = urlparse(id)

    src = "src"
    if parse.scheme and parse.netloc:
        id = escape(id)
        src += "doc"
    return f"""<iframe {src}="{id}" width="{width}" height="{height}"/>"""

def md(body):
    return get_ipython().weave.markdown_renderer.render(body)