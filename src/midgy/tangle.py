"""midgy.tangle is a minimal translation of markdown to python.

markdown tangles to python on indented code blocks [fences]. markdown
blocks are treated translated to python as regular block strings. the
tangled python code represents a line-for-line translate of the markdown.

other implementations can extend these objects to extend their own literate
programming interfaces through the base `markdown-it-py` api.

[fences]: code fences are not in scope for a minimal implementation
"""

from dataclasses import dataclass, field
from io import StringIO
from re import compile
from textwrap import dedent, indent

from markdown_it import MarkdownIt
from markdown_it.renderer import RendererHTML
from markdown_it.renderer import RendererProtocol as Protocol

BLANK, CONTINUATION, COLON, FENCE, SPACE = "", "\\", ":", "```", " "
QUOTES = "'''", '"""'


@dataclass
class Env:
    """the rendering environment for the markdown it rendered"""

    @dataclass
    class IndentState:
        """the indent state during rendering

        the diagram below show the refenerce, trailing, and leading indents relative
        to a markdown block. the indents for the markdown need to be computed relative
        to the enclosing code blocks.

        reference CODECODECODECODECODECODECODECODE
        trailing  CODECODECODECODECODECODECODECODE

        MMMMMMDDDDDDDDDMMMMMMDDDDDDDDDMMMMMMDDDDDDDDD
        MMMMMMDDDDDDDDDMMMMMMDDDDDDDDDMMMMMMDDDDDDDDD
        MMMMMMDDDDDDDDDMMMMMMDDDDDDDDDMMMMMMDDDDDDDDD

        leading        CODECODECODECODECODECODECODE
                  CODECODECODECODECODECODECODE"""

        reference: int = field(
            default=0,
            metadata=dict(
                description="The first indent of the first line of code in a document"
            ),
        )
        trailing: int = field(
            default=0,
            metadata=dict(
                description="The indent of last code line before a markdown block"
            ),
        )
        leading: int = field(
            default=0,
            metadata=dict(
                description="The indent of last code line before a markdown block"
            ),
        )

    @dataclass
    class LastCharacterState:
        """the first non-blank character before a markdown block can change how the
        rendering step behaves. these conditions let us define markdown in python
        variables and write docstrings with markdown"""

        continuation: bool = field(
            default=False,
            metadata=dict(description="The code before the markdown ends with `\\`"),
        )
        colon: bool = field(
            default=False,
            metadata=dict(description="The code before the markdown ends with `:`"),
        )
        quotes: bool = field(
            default=False,
            metadata=dict(
                description="The code before the markdown ends with triple quotes"
            ),
        )
        fence: bool = field(
            default=False,
            metadata=dict(description="The code is inside a markdown fence"),
        )

        def get_state(self, str, **kw):
            """get the last character state of a string"""
            str = str.rstrip()
            kw["continuation"] = str.endswith(CONTINUATION)
            str = str.rstrip(CONTINUATION)
            return dict(colon=str.endswith(COLON), quotes=str.endswith(QUOTES), **kw)

    source: object = field(metadata=dict(description="input code being translated"))
    last_line: int = field(
        default=0, metadata=dict(description="the last code line visited")
    )
    indents: IndentState = field(default_factory=IndentState)
    chars: LastCharacterState = field(default_factory=LastCharacterState)
    noncode_lines: list = field(
        default_factory=list,
        metadata=dict(
            description="lines of input collected while looking for code blocks."
        ),
    )
    terminal_character: str = field(
        default=BLANK,
        metadata=dict(description="trailing character after the non-code block"),
    )


class Tangle(MarkdownIt):
    """tangle is a class that translates markdown to python"""

    def parse(self, src, env=None):
        """parse the source and return the markdown tokens"""
        if env is None:
            env = dict(vars(Env(StringIO(src))))

        return super().parse(src, env)

    def render(self, src, env=None):
        """render the source as translated python"""
        if env is None:
            env = dict(vars(Env(StringIO(src))))

        return super().render(src, env)

    def render_lines(self, src):
        """a shim that includes the tangler in the ipython transformer"""
        return self.render("".join(src)).splitlines(True)

    class Python(Protocol):
        __init__ = RendererHTML.__init__

        class Noncode(str):
            """sentinel class to indicate a string is not code"""

        class NotIndented(str):
            """sentinel class to indicate a string needs indentation"""

        def feed(self, token, options, env):
            return getattr(self, token.type)(token, options, env) or ""

        def render(self, tokens, options, env):
            """render the markdown tokens in a blob of python code."""
            body = StringIO()
            for token in tokens:
                if hasattr(self, token.type):
                    env["noncode_lines"].append(
                        self.Noncode(self.readlines(token.map[0], env))
                    )
                    body.writelines(self.feed(token, options, env))
            else:
                env["noncode_lines"].append(self.Noncode(self.readlines(1e6, env)))
                env["terminal_character"] = ";"
                body.writelines(self.noncode_block(env))

            return dedent(body.getvalue())

        def readline(self, env):
            """read a single line for the source"""
            try:
                return env["source"].readline()
            finally:
                env["last_line"] += 1

        def readlines(self, stop, env):
            """read multiple lines until you want to stop"""
            s = StringIO()
            while env["last_line"] < stop:
                s.writelines(self.readline(env))
            return s.getvalue()

        def code_block(self, token, options, env):
            """render a code block"""
            indents, chars = env["indents"], env["chars"]
            current_line_indent = 0
            last_non_empty_line = BLANK
            found_first_line = False  # false until we find the first code line

            code = StringIO()
            while env["last_line"] < token.map[-1]:
                line = self.readline(env)

                if line.strip():
                    last_non_empty_line = line
                    current_line_indent = _get_num_indent(last_non_empty_line)

                    if not found_first_line:
                        # when we hit the first line we can compute the constraints on
                        if not indents.reference:
                            indents.reference = indents.trailing = current_line_indent
                        indents.leading = current_line_indent

                        # write our noncode as code
                        code.writelines(self.noncode_block(env))

                    found_first_line = True

                code.writelines(line)
            # update the indents based on the last non empty line's trailing characterss
            vars(chars).update(chars.get_state(last_non_empty_line))
            indents.trailing = current_line_indent

            if chars.continuation:
                return _get_continued_code_block(code.getvalue(), current_line_indent)

            return code.getvalue()

        def noncode_block(self, env):
            """unquoted markdown -quote-> unindented string -indent-> python block string"""
            indents, chars = env["indents"], env["chars"]

            noncode = not_indented = BLANK
            noncode_indent = _get_noncode_indent(**env)
            for x in env["noncode_lines"] + [self.NotIndented(BLANK)]:
                if isinstance(x, self.Noncode):
                    noncode += x
                if isinstance(x, self.NotIndented):
                    if chars.quotes:
                        # inside of quotes we only do some indenting
                        noncode = indent(noncode, SPACE * noncode_indent)
                    else:
                        # quote the markdown block
                        noncode = _get_quoted(noncode, noncode_indent, env)
                    # promote unquoted to unindented
                    not_indented += noncode

                    # clear the unquoted buffer
                    noncode = BLANK
                    if x.strip():
                        # add the non empty lines to the unindented block
                        not_indented += SPACE * noncode_indent + x

            env["noncode_lines"].clear()
            return indent(not_indented, SPACE * indents.reference)


def _get_noncode_indent(indents, chars, **_):
    """compute the current indent based on the enclosing blocks"""
    if chars.quotes:  # then we require no adjustment
        indent = indents.trailing
    elif chars.colon:  # then we want to indent things like docstrings
        indent = max(indents.trailing + 4, indents.leading)
    elif indents.leading >= indents.trailing:
        indent = indents.leading  # the leading indent defines the indent
    else:
        indent = indents.trailing  # the trailing indent defines in the indent

    indent -= indents.reference  # remove the reference indent
    return indent


def _get_num_indent(str):
    """get the leading indents of block string"""
    line = StringIO(str).readline()
    return len(line) - len(line.lstrip())


def _get_continued_code_block(input, indent):
    lines = input.splitlines(True)
    end = []
    while lines:
        if not lines[-1].strip():
            end.append(SPACE * indent + CONTINUATION + lines.pop(-1))
        break
    return "".join(lines + list(reversed(end)))


def _get_quoted(input, indent=0, env=None):
    """heuristics that quote a narrative block as a block string."""
    input = dedent(input)
    quote = QUOTES[QUOTES[0] in input]
    quote, l, r = (
        QUOTES[QUOTES[0] in input],
        input.lstrip(),
        input.rstrip(),
    )
    continues = r.endswith(CONTINUATION)
    r = r.rstrip(CONTINUATION)

    if r and (r[-1] == quote[0]):
        quote = QUOTES[QUOTES.index(quote) - 1]
    if not (l or r):
        return input  # this represents the case of a blank string
    begin, end = input[: len(input) - len(l)], input[len(r) :]
    if env["chars"].continuation:
        begin = "".join(map(CONTINUATION.__add__, begin.splitlines(True)))
    if continues:
        end = "".join(_get_continued_code_block(end, indent))
    return (
        begin  # leading whitespace
        + SPACE * indent  # computed indent
        + "r"  # experimental, but i think regular strings make sense
        + quote  # enter block string
        + input[len(input) - len(l) : len(r)]  # code body
        + quote  # exit block string
        + env["terminal_character"]  # computed trailing character
        + end  # trailing whitespace
    )


def load_ipython_extension(shell):
    from traitlets import Instance

    shell.add_traits(tangle=Instance(Tangle, kw=dict(renderer_cls=Tangle.Python)))
    shell.input_transformer_manager.cleanup_transforms.insert(
        0, shell.tangle.render_lines
    )


def unload_ipython_extension(shell):
    if shell.has_trait("tangle"):
        shell.input_transformer_manager.cleanup_transforms = list(
            filter(
                shell.tangle.render_lines.__ne__,
                shell.input_transformer_manager.cleanup_transforms,
            )
        )
