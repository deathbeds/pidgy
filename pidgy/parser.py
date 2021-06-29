"""a markdown parser that returns tokenized inputs

the parser using the `markdown-it-py` machinery to parse markdown,
we chose this approach because the parser returns line numbers. the
`Markdown` tokenizer dispatches different renders based on different 
syntactic considerations.
"""

import functools
import io
import re

import markdown_it

from . import tangle

MAGIC = re.compile(r"^\s*%{2}")


class Markdown(markdown_it.MarkdownIt):
    """a dispatching markdown tokenizer

    the tokenizer creates tokens from a string of markdown with line numbers.
    these tokens are passed to renderer class that exports valid code.
    """

    def __init__(self, *args, **kwargs):
        # initialize the tokenizer as nromal
        super().__init__(*args, **kwargs)

        # add the front matter rule
        [
            self.block.ruler.before(
                "code",
                "front_matter",
                __import__("functools").partial(frontMatter, x),
                {"alt": ["paragraph", "reference", "blockquote", "list"]},
            )
            for x in "-+"
        ]

        # add a rule explicity for doctests
        self.block.ruler.before("code", "doctest", doctest)

        # replace the existing block code one with one that can bail on doctest
        self.block.ruler.disable("code")
        self.block.ruler.after("doctest", "code", code)

        import mdit_py_plugins.footnote

        # add a footnote definition that appends tokens
        self.block.ruler.after(
            "list", "footnote_def", footnote, {"alt": ["paragraph", "reference"]}
        )
        # use out own reference lexer
        self.block.ruler.disable("reference")
        # add a reference definition that appends tokens
        self.block.ruler.after("footnote_def", "", reference)

    def init_env(self, src, env):
        """initialize the env that continues through lexing and rendering"""

        # use a string buffer for efficiency
        env.setdefault("source", io.StringIO(src))

        # accrue unprocesses noncode objects
        env.setdefault("unprocessed", [])

        # last line from the buffer that was read
        env.setdefault("last_line", 0)

    def runner(self, name, src, env=None):
        """a partial method used by both the parse and render methods"""
        # we have to initialize a special environment for this translation
        from .lisp import is_lisp

        # initialize the environment
        if env is None:
            env = {}
        self.init_env(src, env)
        # dispatch different renderes
        if MAGIC.match(src) or is_lisp(src):
            # when magics or lisp like syntaxes are encountered
            # use the null render
            self.renderer_cls = tangle.Null
            self.renderer = tangle.Null()
        else:
            # otherwise we use pidgy's heuristics to render python
            self.renderer_cls = tangle.Python
            self.renderer = tangle.Python()

        # trigger either the parse or rende methods
        return getattr(super(), name)(src, env)

    # parse and render methods for the parser
    parse = functools.partialmethod(runner, "parse")
    render = functools.partialmethod(runner, "render")

    def __call__(self, src):
        # a callable method for the class that lets us use
        # the object as an input transformer in IPython
        return self.render("".join(src)).splitlines(True)

    def print(self, src, env=None):
        """print the rendered source"""
        print(self.render(src, env))


# we wrote our own front matter extension so we can have yaml and toml front matter
# ala jekyll and hugo repsectively.
def frontMatter(marker_str, state, start, end, silent, markers=("+++", "---")):
    """a markdown it lexer for toml and yaml front matter"""
    from math import floor

    if state.tokens:
        return False

    while start < end:
        if state.isEmpty(start):
            start += 1
            continue
        break
    else:
        return False

    marker = None
    line = state.getLines(start, start + 1, 0, True)

    if not state.getLines(start, start + 1, 0, True).startswith(markers):
        return False
    next = start + 1

    marker = markers[line.startswith(markers[1])]
    while next < end:
        line = state.getLines(next, next + 1, 0, True)
        next += 1
        if line.startswith(marker):
            break

    else:
        return False

    old_parent = state.parentType
    old_line_max = state.lineMax
    state.parentType = "container"

    state.lineMax = next

    token = state.push("front_matter", "", 0)
    token.hidden = True
    token.markup = marker
    token.content = state.src[state.bMarks[start] : state.eMarks[next]]
    token.block = True

    state.parentType = old_parent
    state.lineMax = old_line_max
    state.line = next  # + (1 if auto_closed else 0)
    token.map = [start, state.line]

    return True


def doctest(state, start, end, silent=False):
    """a markdown it lexer for doctests"""
    if not state.getLines(start, start + 1, 0, True).lstrip().startswith(">>> "):
        return False

    indent = state.bMarks[start]
    next = start + 1

    while next < end:
        if state.isEmpty(next):
            break

        if state.bMarks[next] < indent:
            break

        next += 1

    state.line = next

    token = state.push("doctest", "code", 0)
    token.content = state.getLines(start, next, 0, True)
    token.map = [start, state.line]
    return True


def code(state, start, end, silent=False):
    """a markdown lexer for code that is aware of doctests"""
    if state.sCount[start] - state.blkIndent < 4:
        return False

    indent = state.bMarks[start]
    last = next = start + 1

    while next < end:
        if state.isEmpty(next):
            next += 1
            continue

        if state.sCount[next] - state.blkIndent >= 4:
            if state.getLines(next, next + 1, 0, True).lstrip().startswith(">>> "):
                break
            next += 1
            last = next
            continue

        break

    state.line = last

    token = state.push("code_block", "code", 0)
    token.content = state.getLines(start, last, 4 + state.blkIndent, True)
    token.map = [start, state.line]
    return True


def reference(state, start, end, silent=False):
    """a reference lexer than inlines the token in the token stream"""
    result = markdown_it.rules_block.reference(state, start, end, silent)
    if not result:
        return result
    for key, value in sorted(
        state.env["references"].items(), key=lambda x: x[1]["map"][0]
    ):
        token = state.push("reference", "span", 0)
        token.content = state.getLines(*value["map"], 0, True)
        token.map = value["map"]
        token.meta.update(value, name=key)
    state.env["references"].clear()

    return result


def footnote(state, start, end, silent=False):
    """a footnote lexer than inlines the token in the token stream"""
    import mdit_py_plugins.footnote

    result = mdit_py_plugins.footnote.index.footnote_def(state, start, end, silent)
    if not result:
        return result
    return result


def load_ipython_extension(shell):
    import traitlets

    shell.add_traits(tangle=traitlets.Any(Markdown()))
    shell.input_transformer_manager.cleanup_transforms.insert(0, shell.tangle)


def unload_ipython_extension(shell):
    shell.input_transformer_manager.cleanup_transforms = [
        x
        for x in shell.input_transformer_manager.cleanup_transforms
        if not isinstance(x, Markdown)
    ]
