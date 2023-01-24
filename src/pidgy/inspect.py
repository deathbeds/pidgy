from . import get_ipython
from traceback import format_exception
from .environment import IPythonTemplate
import sys, types

from traitlets import Any
INSPECT_METHOD = ["do_inspect", "inspect"][sys.platform == "emscripten"]


def inspect_weave(code, cursor_pos, cache={}):
    data = dict(found=True)
    if not code.strip():
        data["data"] = {"text/markdown": help}
    else:
        tokens = cache.get(code)
        line, offset = lineno_at_cursor(code, cursor_pos)
        if tokens is None:
            cache.clear()
            tokens = cache[code] = get_ipython().tangle.parse(code)
        where = get_md_pointer(tokens, line, offset)
        data["data"] = {"text/markdown": f"""`{"/".join(where)}`\n\n{code}"""}
    return data


def lineno_at_cursor(cell, cursor_pos=0):
    offset = 0
    for i, line in enumerate(cell.splitlines(True)):
        next_offset = offset + len(line)
        if not line.endswith("\n"):
            next_offset += 1
        if next_offset > cursor_pos:
            break
        offset = next_offset
    col = cursor_pos - offset
    return i, col


def get_md_pointer(tokens, line, offset):
    where = [f"L{line+1}:{offset+1}"]
    for node in tokens:
        if node.type == "root":
            continue
        if node.map:
            if line < node.map[0]:
                break
            elif node.map[0] <= line < node.map[1]:
                where.append(node.type)
    return where


def get_bangs(cell, cursor_pos):
    if cell[cursor_pos - 1] == "!":
        l, r = cell[:cursor_pos], cell[cursor_pos:]
        return len(l) - len(l.rstrip("!")) + len(r) - len(r.strip("!"))
    return 0


def post_bangs(cell, bangs):
    shell = get_ipython()
    if bangs >= 6:
        result = shell.run_cell(cell, store_history=False, silent=True)
        error = result.error_before_exec or result.error_in_exec
        if error:
            return {
                "text/markdown": f"""```pycon\n{"".join(
                format_exception(type(error), error, error.__traceback__)
            )}\n```"""
            }
        else:
            shell.weave.update()
    if bangs >= 3:
        result = shell.environment.from_string(cell, None, IPythonTemplate)
        return {"text/markdown": result.render()}


def do_inspect(self, cell, cursor_pos, detail_level=1, omit_sections=(), *, cache={}):
    post = post_bangs(cell, get_bangs(cell, cursor_pos))
    if post:
        data = self.original_inspector("", 0, detail_level=0, omit_sections=())
        data["data"] = post
        data["found"] = True
    else:
        data = self.original_inspector(cell, cursor_pos, detail_level=0, omit_sections=())
        if not data["found"]:
            data.update(inspect_weave(cell, cursor_pos))
    return data


def load_ipython_extension(shell):
    if not shell.kernel.has_trait("original_inspector"):
        shell.kernel.add_traits(original_inspector=Any(getattr(shell.kernel, INSPECT_METHOD)))
    setattr(shell.kernel, INSPECT_METHOD, types.MethodType(do_inspect, shell.kernel))


def unload_ipython_extension(shell):
    if shell.kernel.has_trait("original_inspector"):
        setattr(shell.kernel, INSPECT_METHOD, shell.kernel.original_inspector)
