"""translate markdown to python, based on indented code, using markdown it."""

from dataclasses import dataclass, field
from io import StringIO
from re import compile
from textwrap import dedent, indent

from markdown_it import MarkdownIt
from markdown_it.renderer import RendererHTML, RendererProtocol

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
            str = str.rstrip().rstrip(CONTINUATION)
            return dict(colon=str.endswith(COLON), quotes=str.endswith(QUOTES))

    source: StringIO = field(metadata=dict(description="input code being translated"))
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

    class Python(RendererProtocol):
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
            current_line_indent, last_non_empty_line, found_first_line = 0, BLANK, False
            indents, chars, code = env["indents"], env["chars"], StringIO()
            while env["last_line"] < token.map[-1]:
                line = self.readline(env)
                if line.strip():
                    last_non_empty_line = line
                    current_line_indent = _get_num_indent(last_non_empty_line)
                    if not found_first_line:  # we can compute the indent constraints
                        if not indents.reference:  # we initialize all the indents
                            indents.reference = indents.trailing = current_line_indent
                        indents.leading = current_line_indent
                        # write to the buffer our noncode as code
                        code.writelines(self.noncode_block(env))
                    found_first_line = True
                code.writelines(line)
            # update the last character state based on the last line.
            vars(chars).update(chars.get_state(last_non_empty_line))
            indents.trailing = current_line_indent

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
                    if chars.quotes:  # indent the code according
                        noncode = indent(noncode, SPACE * noncode_indent)
                    else:  # quote the markdown block
                        noncode = _get_quoted(noncode, noncode_indent, env)
                    not_indented += noncode  # promote not quoted to not indented

                    # clear the unquoted buffer
                    noncode = BLANK
                    if x.strip():  # add the non empty lines to the unindented block
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


def _get_quoted(input, indent=0, env=None):
    """heuristics that quote a narrative block as a block string."""
    input = dedent(input)
    quote = QUOTES[QUOTES[0] in input]
    quote = QUOTES[QUOTES[0] in input]
    l, r = input.lstrip(), input.rstrip().rstrip(CONTINUATION)
    if r and (r[-1] == quote[0]):
        quote = QUOTES[QUOTES.index(quote) - 1]
    if not (l or r):  # we have a blank string
        return input
    begin, end = input[: len(input) - len(l)], input[len(r) :]
    return (  # recombine all of the parts into quoted python
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
