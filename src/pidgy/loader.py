from importnb import Notebook

from .tangle import Tangle
from .weave import Weave


class Literate(Notebook):
    """an importnb extension for pidgy documents"""

    extensions = ".py.md", ".md", ".md.ipynb"
    tangle = Tangle(renderer_cls=Tangle.Python)
    weave = Weave()

    def get_data(self, path):
        if self.path.endswith(".md"):
            self.source = self.decode()
            return self.code(self.source)
        return super(Literate, self).get_data(path)

    def code(self, str):
        return self.tangle.render("".join(str))

        extensions = ".py.md .md .md.ipynb".split()

    def visit(self, node):
        return node

    get_source = get_data = get_data

    def exec_module(self, module):
        super().exec_module(module)
        module._repr_markdown_ = lambda: self.weave.environment.from_string(
            self.source
        ).render(vars(module))
