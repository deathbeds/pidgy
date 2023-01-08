"""the extras extension adds features that improve interactive computing

1. exposes the `shell` variable for quick access to the interactive instance.
2. each execution the sys modules are populated in the namespace.
  
  this feature minimizes time between computing iterations by bringing more completion sooner.
  in an interactive computing session, the sys modules hold variable names not available to
  the author, but when available help continue flow between executions.

3. IPython display objects are added to the user namespace
4. top-level return statement become IPython.display expressions.
5. it should be easy to copy and paste json for beginners. 
     `true, false and null` are buultins.
"""

import builtins
from ast import Call, Expr, NodeTransformer, Tuple, parse, copy_location, fix_missing_locations
from pathlib import Path
from subprocess import CalledProcessError

import IPython
from traitlets import CUnicode

from . import get_ipython

builtins.true, builtins.false, builtins.null = True, False, None


# happens each execution
def sys_modules_are_part_of_ns():
    from sys import modules

    shell = get_ipython()
    for k in modules:
        if k:
            if k.startswith("_"):
                continue
            if "." in k:
                continue
            shell.user_ns.setdefault(k, modules[k])


# happens once
def ipython_displays_are_part_of_ns(shell):
    from IPython import display
    from IPython.display import DisplayObject, IFrame, TextDisplayObject

    for k, v in vars(display).items():
        if isinstance(v, type) and issubclass(v, (DisplayObject, IFrame)):
            if v not in {DisplayObject, TextDisplayObject}:
                if k[0].isupper():
                    shell.user_ns.setdefault(k, v)
    try:
        ipywidgets_displays_are_part_of_ns(shell)
    except ModuleNotFoundError:
        pass


def ipywidgets_displays_are_part_of_ns(shell):
    import ipywidgets
    from ipywidgets import Widget

    for k, v in vars(ipywidgets).items():
        if isinstance(v, type) and issubclass(v, Widget):
            if k[0].isupper():
                shell.user_ns.setdefault(k, v)


def shebang_transform(lines):
    for i, line in enumerate(map(str.strip, lines)):
        if line:
            if line.startswith(("#!",)):
                lines[i] = lines[0].replace("#!", "%%", 1)
            break
    return lines


def shebang_cell_magic(line, body):
    import tempfile

    from IPython import get_ipython

    shell = get_ipython()
    with tempfile.NamedTemporaryFile(
        prefix=f"ipython-{shell.execution_count}", delete=False, suffix=".py"
    ) as file:
        file.write(body.encode())
    try:
        get_ipython().system(line + " " + file.name)
    except CalledProcessError:
        pass
    finally:
        Path(file.name).unlink()


class ReturnDisplay(NodeTransformer):
    """transform a return node into an IPython display expression"""

    REPLACEMENT = parse('__import__("IPython").display.display', mode="eval")

    def visit_FunctionDef(self, node):
        return node

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Return(self, node):
        return copy_location(
            Expr(
                Call(
                    func=self.REPLACEMENT.body,
                    args=node.value.elts if isinstance(node.value, Tuple) else [node.value],
                    keywords=[],
                )
            ),
            node,
        )


def load_ipython_extension(shell: IPython.InteractiveShell):
    shell.events.register("pre_execute", sys_modules_are_part_of_ns)
    ipython_displays_are_part_of_ns(shell)
    shell.ast_transformers.append(ReturnDisplay())
    shell.input_transformers_cleanup.append(shebang_transform)
    shell.register_magic_function(shebang_cell_magic, "cell", "/usr/bin/env")


def unload_ipython_extension(shell: IPython.InteractiveShell):
    try:
        shell.events.unregister("pre_execute", sys_modules_are_part_of_ns)
    except ValueError:
        pass
    shell.ast_transformers = [x for x in shell.ast_transformers if not isinstance(x, ReturnDisplay)]
    try:
        shell.input_transformers_cleanup.remove(shebang_transform)
    except ValueError:
        pass
