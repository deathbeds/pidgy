import pathlib

import importnb

from . import get_ipython, parser, weave


class Pidgy(importnb.Notebook):
    """an importnb extension for pidgy documents"""

    extensions = ".py.md", ".md", ".md.ipynb"

    def get_data(self, path):
        if self.path.endswith(".md"):
            self.source = self.decode()
            return self.code(self.source)
        return super(Pidgy, self).get_data(path)

    def code(self, str):
        return parser.Markdown().render("".join(str))

        extensions = ".py.md .md .md.ipynb".split()

    def visit(self, node):
        return node

    get_source = get_data = get_data

    def exec_module(self, module):
        super().exec_module(module)
        module._repr_markdown_ = (
            lambda: weave.get_environment()
            .from_string(self.source)
            .render(vars(module))
        )


def load_ipython_extension(shell):
    if globals().get("LOADER") is None:
        globals()["LOADER"] = Pidgy()

    unload_ipython_extension(shell)
    globals()["LOADER"].__enter__()


def unload_ipython_extension(shell):
    if "LOADER" in globals():
        globals()["LOADER"].__exit__()
