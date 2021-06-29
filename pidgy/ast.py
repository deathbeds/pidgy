"""custom ast transformers

* provide top level return syntax ala await"""
import ast
import collections

import traitlets


class Return(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        return node

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Return(self, node):
        replace = ast.parse("""__import__('IPython').display.display()""").body[0]
        replace.value.args = (
            node.value.elts if isinstance(node.value, ast.Tuple) else [node.value]
        )
        return ast.copy_location(replace, node)


def load_ipython_extension(shell):
    shell.ast_transformers.insert(0, Return())


def unload_ipython_extension(shell):
    shell.ast_transformers = [
        x for x in shell.ast_transformers if not isinstance(x, Return)
    ]
