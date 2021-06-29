"""an extension to permit hy python lisp in code blocks"""

import contextlib
import io
import re

import IPython
import markdown_it
import traitlets

from . import get_ipython

HY_MATCH = re.compile(r"(^\s*\().*(\)\s*$)", re.MULTILINE)
LIT_HY_MATCH = re.compile(r"(^\s{4,}\().*(\s{4,}\)\s*$)", re.MULTILINE)
LIT_HY_MATCH = re.compile(r"^\s*\(.*\)\s*$", re.MULTILINE)

def is_lisp(s):
    s = s.strip()
    return s.startswith("(") and s.endswith(")")


class HyCompiler(IPython.core.compilerop.CachingCompiler, traitlets.HasTraits):
    compiler = traitlets.Any()

    @traitlets.default("compiler")
    def dcompiler(self):
        import hy.cmdline

        return hy.cmdline.HyCompile(
            get_ipython().user_module,
            get_ipython().user_ns,
            hy_compiler=hy.cmdline.HyASTCompiler(get_ipython().user_module),
        )

    def ast_parse(self, source, filename="<unknown>", symbol="exec"):
        import hy
        return hy.compiler.hy_compile(
            hy.lex.hy_parse(source), get_ipython().user_module
        )


def pre_run_cell(info):
    s = info.raw_cell.strip()
    if is_lisp(s):
        get_ipython().compiler_class = HyCompiler
        get_ipython().compile = HyCompiler()


def post_run_cell(result):
    if type(get_ipython().compile) is not IPython.core.compilerop.CachingCompiler:
        get_ipython().compiler_class = IPython.core.compilerop.CachingCompiler
        get_ipython().compile = IPython.core.compilerop.CachingCompiler()


def load_ipython_extension(shell):
    shell.events.register(pre_run_cell.__name__, pre_run_cell)
    shell.events.register(post_run_cell.__name__, post_run_cell)


def unload_ipython_extension(shell):
    with contextlib.suppress(ValueError):
        shell.events.unregister(pre_run_cell.__name__, pre_run_cell)
        shell.events.unregister(post_run_cell.__name__, post_run_cell)


def get_quoted(s):
    """returned a block of text wrapped in quotes"""
    l, r = s.lstrip(), s.rstrip()
    if not (l or r):
        return s

    return (
        s[: len(s) - len(l)] + "#[[" + s[len(s) - len(l) : len(r)] + "]]" + s[len(r) :]
    )
