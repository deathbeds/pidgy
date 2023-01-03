from midgy.loader import Markdown

from .extras import ReturnDisplay
from .tangle import IPython


class Pidgy(Markdown):
    """an importnb extension for pidgy documents"""

    extensions = ".py.md", ".md", ".md.ipynb"

    def visit(self, node):
        return super().visit(ReturnDisplay().visit(node))
