from importnb import Notebook

from .tangle import Python
from .markdown import Renderer
from .extras import ReturnDisplay


class Markdown(Notebook):
    """an importnb extension for pidgy documents"""

    extensions = ".py.md", ".md", ".md.ipynb"
    tangle = Renderer(renderer_cls=Python)

    def get_data(self, path):
        if self.path.endswith(".md"):
            self.source = self.decode()
            return self.code(self.source)
        return super(Notebook, self).get_data(path)

    def code(self, str):
        return super().code(self.tangle.render("".join(str)))

    def visit(self, node):
        return super().visit(ReturnDisplay().visit(node))

    get_source = get_data = get_data
