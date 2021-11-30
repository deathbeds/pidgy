"""models.py contains models for holding state during parsing."""

from dataclasses import dataclass
from io import StringIO
from re import compile
from typing import Pattern

from .utils import dataclass, field

BLANK, CONTINUATION, COLON, FENCE, SPACE = "", "\\", ":", "```", " "
QUOTES = "'''", '"""'
CELL_MAGIC, DOCTEST_LINE = compile("^\s*%{2}\S"), compile("^\s*>{3}\s+")
DOCTEST_CHAR, CONTINUATION_CHAR, COLON_CHAR, QUOTES_CHARS = 62, 92, 58, {39, 34}
_RE_BLANK_LINE = compile(r"^\s*\r?\n")


@dataclass
class Env:
    """the rendering environment for the markdown it rendered"""

    @dataclass
    class IndentState:
        """the indent state relative to a markdown block    .

        the diagram below show the refenerce, trailing, and leading indents relative
        to a markdown block. the indents for the markdown need to be computed relative
        to the enclosing code blocks.

        reference CODECODECODECODECODECODECODECODE
        trailing  CODECODECODECODECODECODECODECODE

        MMMMMMDDDDDDDDDMMMMMMDDDDDDDDDMMMMMMDDDDDDDDD
        MMMMMMDDDDDDDDDMMMMMMDDDDDDDDDMMMMMMDDDDDDDDD

        leading        CODECODECODECODECODECODECODE
                CODECODECODECODECODECODECODE"""

        reference: int = field(
            0, "The first indent of the first line of code in a document"
        )
        trailing: int = field(0, "The indent of last code line before a markdown block")
        leading: int = field(0, "The indent of last code line before a markdown block")

    @dataclass
    class LastCharacterState:
        """the first non-blank character before a markdown block can change how the
        rendering step behaves. these conditions let us define markdown in python
        variables and write docstrings with markdown"""

        colon: bool = field(False, "The code before the markdown ends with `:`")
        quotes: bool = field(
            False, "The code before the markdown ends with triple quotes"
        )

    source: StringIO = field(None, "input code being translated")
    last_line: int = field(0, "the last code line visited")
    indents: IndentState = field(IndentState)
    chars: LastCharacterState = field(LastCharacterState)
    terminal_character: str = field(
        BLANK, "trailing character after the non-code block"
    )


@dataclass
class Weave:
    template: bool = field(True, "flag to render the output with or without jinja")
    asynch: bool = field(False, "use the async loop for reactive changes")
    reactive: bool = field(False, "reactive templates with the namespace.")
    no_show: Pattern = field(_RE_BLANK_LINE, "the pattern for suppressing output")
    ansi: bool = field(False, "weave input to monospace ansi formatted text w/ rich")
    display_cls: type = field(None)
    debug: bool = field(False)
    doctest: bool = field(False, """run doctests on the input""")
