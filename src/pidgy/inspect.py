"""a modified ipython inspector that gives keystroke resolution rendering."""

from . import get_ipython
from functools import lru_cache, partial
from io import StringIO
import sys, types
from traitlets import Any
from pathlib import Path

INSPECT_METHOD = ["do_inspect", "inspect"][sys.platform == "emscripten"]
from itertools import chain
from contextlib import suppress

DIR = Path(__file__).parent
HELP = DIR / "help"


# the do_inspect method overrides kernel inspection in lab and lite.
def do_inspect(self, cell, cursor_pos, detail_level=1, omit_sections=(), *, cache={}):
    return get_ipython().markdown_inspector.inspect(cell, cursor_pos)


def load_ipython_extension(shell):
    if not shell.kernel.has_trait("original_inspector"):
        shell.kernel.add_traits(original_inspector=Any(getattr(shell.kernel, INSPECT_METHOD)))
    if not shell.has_trait("markdown_inspector"):
        shell.add_traits(markdown_inspector=Any(MarkdownInspector()))

    # we can just modify the shell inspector because that is responsible for discovery
    # objects in the run time. we need to intercept the inspection before it passe sinfo to ipython
    setattr(shell.kernel, INSPECT_METHOD, types.MethodType(do_inspect, shell.kernel))


def unload_ipython_extension(shell):
    if shell.kernel.has_trait("original_inspector"):
        setattr(shell.kernel, INSPECT_METHOD, shell.kernel.original_inspector)


class MarkdownInspector:
    def prepare(self, body):
        return dict(found=True, status="ok", data={"text/markdown": body}, metadata={})

    def inspect(self, code, cursor_pos=0, cache={}):
        tokens = cache.get(code)
        line, offset = lineno_at_cursor(code, cursor_pos)

        if tokens is None:
            cache.clear()
            tokens = cache.setdefault(code, get_ipython().tangle.parse(code))

        where = get_md_token(tokens, line, offset)
        location = f"`L{line+1}:{offset+1}@" + "/".join(x.type for x in where) + "`" + "\n" * 3
        if where:
            explicit = self.visit(where[-1], code, line, offset, cursor_pos)
            if explicit:
                if isinstance(explicit, dict):
                    shell = get_ipython()
                    if "text/html" in explicit.get("data", {}):
                        explicit["data"]["text/html"] = (
                            shell.weave.markdown_renderer.render(location)
                            + explicit["data"]["text/html"]
                        )
                    return explicit
                return self.prepare(location + explicit)
        if code.strip():
            shell = get_ipython()
            out = location + code
            if shell.tangle.env.get("references"):
                # append any prior markdown references
                out += shell.weave._append_references(code)
            return self.prepare(out)
        return self.prepare(get_pidgy_help())

    def visit(self, node, code, line, offset, cursor_pos):
        with suppress(AttributeError):
            return getattr(self, f"visit_{node.type}")(node, code, line, offset, cursor_pos)

    def visit_fence(self, node, code, line, offset, cursor_pos):
        if node.info:
            if node.info in get_ipython().tangle.include_code_fences:
                return self.visit_code_block(node, code, line, offset, cursor_pos)
            with suppress(AttributeError):
                return getattr(self, f"fence_{node.info}")(node, code, line, offset, cursor_pos)

    def fence_mermaid(self, node, code, line, offset, cursor_pos):
        if line == node.map[0]:
            return get_mermaid_help()
        return self.get_sliced_code(node, code)

    def visit_code_block(self, node, code, line, offset, cursor_pos):
        detail = 0
        if code[cursor_pos - 1] == "?":
            detail += 1
        data = get_ipython().kernel.original_inspector(code, cursor_pos, detail_level=detail)
        if data["found"]:
            return data

    def get_sliced_code(self, node, code):
        body = StringIO()
        for i, line in enumerate(StringIO(code)):
            if node.map[0] <= i < node.map[1]:
                body.write(line)
            if i > node.map[1]:
                break
        return body.getvalue()


@lru_cache
def get_help(name):
    return (DIR / "help" / f"{name}.md").read_text()


get_mermaid_help = partial(get_help, "mermaid")
get_pidgy_help = partial(get_help, "pidgy")


def lineno_at_cursor(cell, cursor_pos=0):
    i = offset = 0
    for i, line in enumerate(cell.splitlines(True)):
        next_offset = offset + len(line)
        if not line.endswith("\n"):
            next_offset += 1
        if next_offset > cursor_pos:
            break
        offset = next_offset
    col = cursor_pos - offset
    return i, col


def get_md_token(tokens, line, offset):
    """return the md token stack corresponding to the cursor position."""
    where = []
    for node in tokens:
        if node.type == "root":
            continue
        if node.map:
            if line < node.map[0]:
                break
            elif node.map[0] <= line < node.map[1]:
                where.append(node)
    return where
