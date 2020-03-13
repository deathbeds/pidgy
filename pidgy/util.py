import re, typing, glob, pathlib


class ContextDepth:
    depth = 0

    def __enter__(self):
        self.depth += 1

    def __exit__(self, *e):
        self.depth -= 1


(FENCE, CONTINUATION, SEMI, COLON, MAGIC, DOCTEST), QUOTES, SPACE = (
    "``` \\ ; : %% >>>".split(),
    ('"""', "'''"),
    " ",
)
WHITESPACE = re.compile("^\s*", re.MULTILINE)


def num_first_indent(text: str) -> int:
    for str in text.splitlines():
        if str.strip():
            return len(str) - len(str.lstrip())
    return 0


def num_last_indent(text: str) -> int:
    for str in reversed(text.splitlines()):
        if str.strip():
            return len(str) - len(str.lstrip())
    return 0


def base_indent(tokens: typing.List[dict]) -> int:
    "Look ahead for the base indent."
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
    """wrap text in `QUOTES`"""
    if text.strip():
        left, right = len(text) - len(text.lstrip()), len(text.rstrip())
        quote = QUOTES[(text[right - 1] in QUOTES[0]) or (QUOTES[0] in text)]
        return text[:left] + quote + text[left:right] + quote + text[right:]
    return text


def num_whitespace(text: str) -> int:
    return len(text) - len(text.lstrip())


def whiten(text: str) -> str:
    """`whiten` strips empty lines because the `markdown.BlockLexer` doesn't like that."""
    return "\n".join(x.rstrip() for x in text.splitlines())


def strip_front_matter(text, sep=None):
    if text.startswith("---\n"):
        front_matter, sep, rest = text[4:].partition("\n---")
    if sep:
        return "".join(rest.splitlines(True)[1:])
    return text


def ansify(str: str, format="markdown"):
    import pygments.formatters.terminal256

    return pygments.highlight(
        str,
        pygments.lexers.find_lexer_class_by_name(format)(),
        pygments.formatters.terminal256.Terminal256Formatter(),
    )


def yield_files(files):
    for file in files:
        yield from map(pathlib.Path, glob.glob(file) if "*" in file else [file])
