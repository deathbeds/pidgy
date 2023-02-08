"""tangle.py provides the Markdown to Python translation model.
"""
import ast
import dis
import types
from dataclasses import dataclass, field
from io import StringIO
from re import MULTILINE, compile
from urllib.parse import urlparse

from midgy.python import Python

from . import get_cell_id, get_ipython

# an instance of this class is used to transform markdown to valid python
# in the ipython extension. the python conversion is constrained by being
# a line for line transformation using indent code blocks (not code fences)
# as references for translating the markdown to valid python objects.

IS_MAGIC = compile("^\s*%{2}", MULTILINE)


def set_current_execution(shell):
    if shell.has_trait("pidgy"):
        id = get_cell_id(shell)
        if shell.pidgy.current_execution:
            if shell.pidgy.current_execution.id == id:
                return
        shell.pidgy.current_execution = Execution(id)


def pidgy_render_lines(lines):
    shell = get_ipython()
    set_current_execution(shell)

    lines = "".join(lines)
    if IS_MAGIC.match(lines):
        return lines.splitlines(True)

    tokens = shell.tangle.parse(lines)
    if hasattr(shell, "current_execution"):
        shell.current_execution.tokens = tokens
        
    shell.current_execution.py = shell.tangle.render_tokens(tokens, src=lines)
    return shell.current_execution.py.splitlines(True)



@dataclass
class IPython(Python):
    """a markdown to python transpiler meant o be used in IPython"""

    parent: object = field(default_factory=get_ipython)
    last_tokens: list = None
    env: dict = field(default_factory=dict)
    URL_PROTOCOLS = "file", "http", "https"
    VALID_URL_LIST_TOKENS = {
        "paragraph_open",
        "paragraph_close",
        "bullet_list_open",
        "bullet_list_close",
        "list_item_open",
        "list_item_close",
    }

    @classmethod
    def get_url_list(cls, tokens):
        urls = []
        for token in tokens:
            if token.type in cls.VALID_URL_LIST_TOKENS:
                continue
            elif token.type == "inline":
                for line in StringIO(token.content):
                    parsed = urlparse(line)
                    if parsed.netloc in cls.URL_PROTOCOLS:
                        urls.append(line.strip())
                        continue
                    break
                else:
                    continue
                break
            break
        else:
            return urls

    def parse(self, src):
        get_ipython().current_execution.md_env = env = dict()
        tokens = super().parse(src, env)
        refs, dups = env.get("references"), env.get("duplicates_refs")
        if refs:
            self.env.setdefault("references", refs).update(refs)
        if dups:
            self.env.setdefault("duplicates_refs", [])
            self.extend(dups)
        return tokens


def load_ipython_extension(shell):
    from . import current
    from traitlets import Instance

    def tangle(line, cell):
        print(shell.tangle.render(cell))

    def parse(line, cell):
        print(shell.tangle.parse(cell))

    shell.add_traits(tangle=Instance(IPython, ()))
    shell.input_transformer_manager.cleanup_transforms.insert(0, pidgy_render_lines)
    shell.register_magic_function(tangle, "cell")
    shell.register_magic_function(parse, "cell")
    current.load_ipython_extension(shell)


def unload_ipython_extension(shell):
    from . import current
    try:
        shell.input_transformer_manager.cleanup_transforms.remove(pidgy_render_lines)
    except ValueError:
        pass
    current.load_ipython_extension(shell)
