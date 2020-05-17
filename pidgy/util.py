"""Code I am not proud of 🤗"""

import re, typing, glob, pathlib, contextlib, sys, textwrap, doctest, markdown_it.extensions.front_matter, markdown_it.extensions.footnote, copy

list_item = re.compile(
    r"^(( *)(?:[*+-]|\d+\.) [^\n]*(?:\n(?!\2(?:[*+-]|\d+\.) )[^\n]*)*)",
    re.MULTILINE | re.UNICODE,
)
footnote_item = re.compile(
    r"\[\^([^\]]+)\]: *([^\n]*(?:\n+|$)(?: {1,}[^\n]*(?:\n+|$))*)", re.UNICODE
)
link_item = re.compile(
    r' *\[([^^\]]+)\]: *<?([^\s>]+)>?(?: +["(]([^\n]+)[")])? *(?:\n+|$)', re.UNICODE
)


class ContextDepth:
    """Count the current depth of a context manager invocation."""

    depth = 0

    def __enter__(self):
        self.depth += 1

    def __exit__(self, *e):
        self.depth -= 1


def html_comment(text):
    return f"""<!--\n{text}\n\n-->"""


def istype(object, cls):
    return isinstance(object, type) and issubclass(object, cls)


(FENCE, CONTINUATION, SEMI, COLON, MAGIC, DOCTEST), QUOTES, SPACE = (
    "``` \\ ; : %% >>>".split(),
    ('"""', "'''"),
    " ",
)
WHITESPACE = re.compile("^\s*", re.MULTILINE)


def indents(str: str) -> int:
    return len(str) - len(str.lstrip())


def num_first_indent(text: str) -> int:
    """The number of indents for the first blank line."""
    for str in text.splitlines():
        if str.strip():
            return indents(str)
    return 0


def num_last_indent(text: str) -> int:
    """The number of indents for the last blank line."""
    for str in reversed(text.splitlines()):
        if str.strip():
            return indents(str)
    return 0


def base_indent(tokens: typing.List[dict]) -> int:
    "Peek into mistune tokens and find the last code indent."
    for i, token in enumerate(tokens):
        if token["type"] == "code":
            code = token["text"]
            if code.lstrip().startswith(FENCE):
                continue
            indent = num_first_indent(code)
            break
    else:
        indent = 4
    return indent


def quote(text: str, trailing="") -> str:
    """Wrap strings in triple quoted block strings."""
    if text.strip():
        left, right = len(text) - len(text.lstrip()), len(text.rstrip())
        quote = QUOTES[(text[right - 1] in QUOTES[0]) or (QUOTES[0] in text)]
        cont = ""
        slug = text[left:right]
        if slug.endswith(CONTINUATION):
            cont = CONTINUATION
            slug = slug.rstrip(CONTINUATION)
        return text[:left] + quote + slug + quote + trailing + cont + text[right:]
    return text


def whiten(text: str) -> str:
    """`whiten` strips empty lines because the `markdown.BlockLexer` doesn't like that."""
    return "\n".join(x.rstrip() for x in text.splitlines())


def strip_front_matter(text: str, sep=None) -> str:
    """Remove yaml front matter froma string."""
    if text.startswith("---\n"):
        front_matter, sep, rest = text[4:].partition("\n---")
    if sep:
        return "".join(rest.splitlines(True)[1:])
    return text


def ansify(str: str, format="md"):
    """High source to be printed in the terms."""
    import pygments.formatters.terminal256

    return pygments.highlight(
        str,
        pygments.lexers.find_lexer_class_by_name(format)(),
        pygments.formatters.terminal256.Terminal256Formatter(),
    )


def yield_files(files: typing.Sequence[str], recursive=False) -> typing.Generator:
    """Return a list of files from a collection of files and globs."""
    for file in files:
        yield from map(
            pathlib.Path,
            getattr(glob, ["", "r"][recursive] + "glob")(str(file))
            if "*" in str(file)
            else [file],
        )


@contextlib.contextmanager
def argv(*args: str):
    argv = sys.argv
    if len(args) == 1 and isinstance(args[0], str):
        args = args[0].split()
    sys.argv = list(args)
    yield
    sys.argv = list(argv)


def strip_shebang(str):
    return re.sub(re.compile(r"#!/.+\n"), "", str)


def strip_html_comment(str):
    return re.sub("(<!--[\s\S]*-->?)", "", str)


def strip_front_matter(text: str, sep=None) -> str:
    """Remove yaml front matter froma string."""
    for sep in "--- +++".split():
        if text.startswith(f"{sep}\n"):
            front_matter, sep, rest = text[4:].partition(f"\n{sep}\n")
            if sep:
                return "".join(rest.splitlines(True)[1:])
    return text


@contextlib.contextmanager
def sys_path():
    root = "." in sys.path
    if root:
        sys.path = ["."] + sys.path
    yield
    if root:
        sys.path.pop(sys.path.index("."))


def pidgy_builtins():
    import IPython, toolz, poser

    return {
        **{
            k: v
            for k, v in vars(IPython.display).items()
            if istype(v, IPython.core.display.DisplayObject)
        },
        **toolz.valfilter(callable, vars(toolz)),
        "shell": IPython.get_ipython(),
        "λ": poser.λ,
        "Λ": poser.Λ,
    }


def clean_doctest_traceback(str, *lines):
    *_, str = str.partition("-" * 70)
    return str.lstrip()


from math import floor
import functools

from markdown_it import MarkdownIt
from markdown_it.rules_block import StateBlock
from markdown_it.common.utils import charCodeAt


def frontMatter(
    marker_str, state: StateBlock, startLine: int, endLine: int, silent: bool
):

    min_markers = 3
    marker_char = charCodeAt(marker_str, 0)
    marker_len = len(marker_str)

    auto_closed = False
    start = state.bMarks[startLine] + state.tShift[startLine]
    maximum = state.eMarks[startLine]

    # Check out the first character of the first line quickly,
    # this should filter out non-front matter
    if startLine != 0 or marker_char != charCodeAt(state.src, 0):
        return False

    # Check out the rest of the marker string
    # while pos <= 3
    pos = start + 1
    while pos <= maximum:
        if marker_str[(pos - start) % marker_len] != state.src[pos]:
            start_content = pos + 1
            break
        pos += 1

    marker_count = floor((pos - start) / marker_len)

    if marker_count < min_markers:
        return False

    pos -= (pos - start) % marker_len

    # Since start is found, we can report success here in validation mode
    if silent:
        return True

    # Search for the end of the block
    nextLine = startLine

    while True:
        nextLine += 1
        if nextLine >= endLine:
            # unclosed block should be autoclosed by end of document.
            return False

        if state.src[start:maximum] == "...":
            break

        start = state.bMarks[nextLine] + state.tShift[nextLine]
        maximum = state.eMarks[nextLine]

        if start < maximum and state.sCount[nextLine] < state.blkIndent:
            # non-empty line with negative indent should stop the list:
            # - ```
            #  test
            break

        if marker_char != charCodeAt(state.src, start):
            continue

        if state.sCount[nextLine] - state.blkIndent >= 4:
            # closing fence should be indented less than 4 spaces
            continue

        pos = start + 1
        while pos < maximum:
            if marker_str[(pos - start) % marker_len] != state.src[pos]:
                break
            pos += 1

        # closing code fence must be at least as long as the opening one
        if floor((pos - start) / marker_len) < marker_count:
            continue

        # make sure tail has spaces only
        pos -= (pos - start) % marker_len
        pos = state.skipSpaces(pos)

        if pos < maximum:
            continue

        # found!
        auto_closed = True
        break

    old_parent = state.parentType
    old_line_max = state.lineMax
    state.parentType = "container"

    # this will prevent lazy continuations from ever going past our end marker
    state.lineMax = nextLine

    token = state.push("front_matter", "", 0)
    token.hidden = True
    token.markup = marker_str * min_markers
    token.content = state.src[state.bMarks[startLine] : state.eMarks[nextLine]]
    token.block = True
    token.meta = state.src[start_content : start - 1]

    state.parentType = old_parent
    state.lineMax = old_line_max
    state.line = nextLine + (1 if auto_closed else 0)
    token.map = [startLine, state.line]

    return True


def enforce_blanklines(str):
    """Make sure blank lines are blank."""
    str = "".join(
        line if line.strip() else "\n" for line in "".join(str).splitlines(True)
    )
    if not str.endswith("\n"):
        str += "\n"
    return str


def quote_docstrings(str):
    next, end = "", 0
    for m in doctest.DocTestParser._EXAMPLE_RE.finditer(str):
        next += str[slice(end, m.start())] + quote(
            str[slice(m.start(), m.end())], trailing=";"
        )
        end = m.end()
    if next:
        next += str[m.end() :]
    return next or str


def lead_indent(str):
    """Count the lead indent of a string"""
    if not isinstance(str, list):
        str = str.splitlines(True)
    for line in str:
        if line.strip():
            return len(line) - len(line.lstrip())
    return 0


def trailing_indent(str):
    """Count the lead indent of a string"""
    if not isinstance(str, list):
        str = str.splitlines(True)
    for line in reversed(str):
        if line.strip():
            return len(line) - len(line.lstrip())
    return 0


def unfence(str):
    """Remove code fences froma string."""
    return "".join("".join(str.split("```", 1)).rsplit("```", 1))


def dedent_block(str):
    """Dedent a block of non code."""
    str = textwrap.dedent(str)
    lines = str.splitlines(True)
    for i, line in enumerate(lines):
        if line.strip():
            lines[i] = textwrap.dedent(line)
            break
    return "".join(lines)


CODE_TYPES = "fence code_block front_matter bullet_list_open ordered_list_open footnote_reference_open reference".split()


def filter_tangle_tokens(token, code=None):
    """Filter out tokens that reference a potential coded object."""
    code = code or []
    if isinstance(token, list):
        for token in token:
            code = filter_tangle_tokens(token, code)
    if token.children:
        for token in token.children:
            code = filter_tangle_tokens(token, code)
    token.type in CODE_TYPES and token not in code and code.append(token)
    if code and (code[-1].type == "fence") and code[-1].info:
        code.pop(-1)
    return code or [
        markdown_it.utils.AttrDict(type="code_block", content="", map=(0, 0))
    ]


def make_reference_tokens(env, *tokens):
    """Turn references in the markdown_it environment to tokens."""
    for reference in env.get("references", {}).values():
        if not tokens:
            tokens += (markdown_it.token.Token("reference", "", 1),)
            tokens[-1].map = reference["map"]
            continue
        for line in env["src"][tokens[-1].map[1] : reference["map"][0]]:
            if line.strip():
                tokens += (markdown_it.token.Token("reference", "", 1),)
                tokens[-1].map = reference["map"]
                break
        else:
            tokens[-1].map[1] = reference["map"][1]

        tokens[-1].content = "".join(env["src"][slice(*tokens[-1].map)])

    return [recontent(x, env) for x in tokens if int.__sub__(*x.map)]


def recontent(token, env):
    """Update the content on a call."""
    token.content = "".join(env["src"][slice(*token.map)])
    return token


def reconfigure_tokens(tokens, env):
    """Tokens are miss ordered, this function splits and orders cells."""
    tokens = sorted(tokens + make_reference_tokens(env), key=lambda x: x.map[0])
    new = tokens and [tokens[0]] or []
    for token in tokens[1:]:
        if token.map[0] < new[-1].map[1]:
            new.extend([token, copy.deepcopy(new[-1])])
            new[-3].map[1], new[-1].map[0] = token.map

            for i in [-3, -1]:
                (
                    new.pop(i)
                    if int.__sub__(*new[i].map) == 0
                    else recontent(new[i], env)
                )
            continue
        new.append(token)

    return [x for x in new if int.__sub__(*x.map)]


def continuation(str, env):
    """Extend a line ending with a continuation."""
    lines, continuing = str.splitlines(), False
    for i, line in enumerate(lines):
        if line.strip():
            continuing = line.endswith("\\")
        elif continuing:
            lines[i] = " " * env["base_indent"] + "\\"
    return "\n".join(lines)


class BaseRenderer:
    """
>>> md = Tangle(renderer_cls=BaseRenderer)
>>> assert len(md.render(s).splitlines()) == len(s.splitlines())
    
    """

    __output__ = "html"
    __init__ = markdown_it.renderer.RendererHTML.__init__

    def render(self, tokens, options, env):
        return "".join(env["src"])
