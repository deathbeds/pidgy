"jinja2 filters that make writing pidgy more fun"

from . import get_ipython
def q(q, cite):
    """a filter for <q>uotes"""
    return f"""<q cite="{cite}">{q}</q>"""


def md(body):
    return get_ipython().weave.markdown_renderer.render(body)