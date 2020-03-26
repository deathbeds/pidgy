import re, typing, glob, pathlib, contextlib, sys


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


def quote(text: str) -> str:
    """Wrap strings in triple quoted block strings."""
    if text.strip():
        left, right = len(text) - len(text.lstrip()), len(text.rstrip())
        quote = QUOTES[(text[right - 1] in QUOTES[0]) or (QUOTES[0] in text)]
        return text[:left] + quote + text[left:right] + quote + text[right:]
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


def ansify(str: str, format="markdown"):
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
    if text.startswith("---\n"):
        front_matter, sep, rest = text[4:].partition("\n---")
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
