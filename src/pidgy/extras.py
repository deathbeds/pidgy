"""the extras extension adds features that improve interactive computing

1. exposes the `shell` variable for quick access to the interactive instance.
2. each execution the sys modules are populated in the namespace.
  
  this feature minimizes time between computing iterations by bringing more completion sooner.
  in an interactive computing session, the sys modules hold variable names not available to
  the author, but when available help continue flow between executions.

3. IPython display objects are added to the user namespace
4. top-level return statement become IPython.display expressions.
"""

from sys import modules
from ast import NodeTransformer, Call, Expr, parse, Tuple
import IPython


def update_sys_modules():
    """update the shell's user namespace to include imported modules"""
    shell = IPython.get_ipython()
    shell.user_ns.update(
        (k, v)
        for k, v in modules.items()
        if k and k[0] != "_" and "." not in k and k not in shell.user_ns
    )


def ipython_display_objects(**data):
    """extract the display object from IPython"""
    from IPython import display
    from IPython.display import DisplayObject, TextDisplayObject, IFrame

    for k, v in vars(display).items():
        if isinstance(v, type) and issubclass(v, (DisplayObject, IFrame)):
            if v not in {DisplayObject, TextDisplayObject}:
                if k[0].isupper():
                    data[k] = v
    return data


class ReturnDisplay(NodeTransformer):
    """transform a return node into an IPython display expression"""

    def visit_FunctionDef(self, node):
        return node

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Return(self, node):
        return Expr(
            Call(
                func=parse('__import__("IPython").display.display', mode="eval").body,
                args=node.value.elts if isinstance(node.value, Tuple) else [node.value],
                keywords=[],
            )
        )


def load_ipython_extension(shell: IPython.InteractiveShell):
    shell.user_ns.setdefault("shell", shell)
    shell.user_ns.update(
        (k, v) for k, v in ipython_display_objects().items() if k not in shell.user_ns
    )
    shell.events.register("pre_execute", update_sys_modules)
    shell.ast_transformers.append(ReturnDisplay())


def unload_ipython_extension(shell: IPython.InteractiveShell):
    shell.events.unregister("pre_execute", update_sys_modules)

    pops = []
    for i, x in enumerate(shell.ast_transformers):
        isinstance(x, ReturnDisplay) and pops.append(i)

    for pop in pops:
        shell.ast_transformers.pop(pop)
