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
from ast import Call, Expr, NodeTransformer, Tuple, parse
from pathlib import Path
from subprocess import CalledProcessError
from sys import modules

import IPython
from traitlets import CUnicode

from .pidgy import Extension

builtins.true, builtins.false, builtins.null = True, False, None


class SysModules(Extension):
    def pre_execute(self):
        """update the shell's user namespace to include imported modules"""
        for k in modules:
            if k:
                if k.startswith("_"):
                    continue
                if "." in k:
                    continue
                self.shell.user_ns.setdefault(k, modules[k])


class IPythonDisplays(Extension):
    def load_ipython_extension(self):
        """extract the display object from IPython"""
        from IPython import display
        from IPython.display import DisplayObject, IFrame, TextDisplayObject

        for k, v in vars(display).items():
            if isinstance(v, type) and issubclass(v, (DisplayObject, IFrame)):
                if v not in {DisplayObject, TextDisplayObject}:
                    if k[0].isupper():
                        self.shell.user_ns.setdefault(k, v)


class Shebang(Extension):
    alias = CUnicode("/usr/bin/env")

    def cleanup_transforms(self, lines):
        for i, line in enumerate(map(str.strip, lines)):
            if line:
                if line.startswith(("#!",)):
                    lines[i] = lines[0].replace("#!", "%%", 1)
                break
        return lines

    def cell(self, argv, body):
        import tempfile

        from IPython import get_ipython

        shell = get_ipython()
        with tempfile.NamedTemporaryFile(
            prefix=f"ipython-{shell.execution_count}", delete=False, suffix=".py"
        ) as file:
            file.write(body.encode())
        try:
            get_ipython().system(argv + " " + file.name)
        except CalledProcessError:
            pass
        finally:
            Path(file.name).unlink()


class ReturnDisplay(Extension, NodeTransformer):
    """transform a return node into an IPython display expression"""

    REPLACEMENT = parse(
        Extension.IS_IPY and '__import__("IPython").display.display' or "print",
        mode="eval",
    )

    def visit_FunctionDef(self, node):
        return node

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Return(self, node):
        return Expr(
            Call(
                func=self.REPLACEMENT.body,
                args=node.value.elts if isinstance(node.value, Tuple) else [node.value],
                keywords=[],
            )
        )


def load_ipython_extension(shell: IPython.InteractiveShell):
    SysModules(shell=shell).load_ipython_extension()
    IPythonDisplays(shell=shell).load_ipython_extension()
    ReturnDisplay(shell=shell).load_ipython_extension()
    Shebang(shell=shell).load_ipython_extension()


def unload_ipython_extension(shell: IPython.InteractiveShell):
    SysModules(shell=shell).unload_ipython_extension()
    IPythonDisplays(shell=shell).unload_ipython_extension()
    ReturnDisplay(shell=shell).unload_ipython_extension()
    Shebang(shell=shell).unload_ipython_extension()
