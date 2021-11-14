"""``midgy``s approach to converting markdown to python
-------------------------------

``midgy``s novelty comes from its heuristics for converting markdown into python code.
unlike most literate programming implementations, ``midgy``s approach relies on indented
code blocks defining a powerful metalanguage that allows markdown and python to cooperate
in a literate documentation.
"""
from io import StringIO
from textwrap import dedent, indent

from markdown_it import MarkdownIt

from .models import BLANK, CELL_MAGIC, CONTINUATION, DOCTEST_LINE, QUOTES, SPACE, Env

__all__ = ("tangle",)


def doctest(state, start, end, silent=False):
    """diverging from the commonmark standard"""
    if DOCTEST_LINE.match(state.getLines(start, start + 1, 0, True)):
        indent, next = state.bMarks[start], start + 1
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
    return False


def code(state, start, end, silent=False):
    """to accomodate doctests we need modify `markdown_it`s convetionally
    block code analyzer"""
    if state.sCount[start] - state.blkIndent >= 4:
        last = next = start + 1
        while next < end:
            if state.isEmpty(next):
                next += 1
            elif state.sCount[next] - state.blkIndent >= 4:
                if DOCTEST_LINE.match(state.getLines(next, next + 1, 0, True)):
                    break
                next += 1
                last = next
            else:
                break
        state.line = last
        token = state.push("code_block", "code", 0)
        token.content = state.getLines(start, last, 4 + state.blkIndent, True)
        token.map = [start, state.line]
        return True
    return False


class Tangle(MarkdownIt):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("renderer_cls", Tangle.Python)
        super().__init__(*args, **kwargs)
        self.block.ruler.before("code", "doctest", doctest)
        self.block.ruler.disable("code")
        self.block.ruler.after("doctest", "code", code)

    def parse(self, src, env=None):
        """parse the source and return the markdown tokens"""
        if env is None:
            env = dict(vars(Env(source=StringIO(src))))

        return super().parse(src, env)

    def render(self, src, env=None):
        """render the source as translated python"""
        if CELL_MAGIC.match(src):
            return src
        if env is None:
            env = dict(vars(Env(source=StringIO(src))))

        return super().render(src, env)

    def render_lines(self, src):
        """a shim that includes the tangler in the ipython transformer"""
        return self.render("".join(src)).splitlines(True)

    from markdown_it.renderer import RendererProtocol

    class Python(RendererProtocol):
        from markdown_it.renderer import RendererHTML

        __init__ = RendererHTML.__init__

        class Noncode(str):
            """sentinel class to indicate a string is not code"""

        class NotIndented(str):
            """sentinel class to indicate a string needs indentation"""

        def feed(self, token, options, env):
            return getattr(self, token.type)(token, options, env) or ""

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
                env["noncode_lines"].append(self.Noncode("".join(env["source"])))
                env["terminal_character"] = ";"
                body.writelines(self.noncode_block(env))

            return dedent(body.getvalue())

        def code_block(self, token, options, env):
            """render a code block"""
            current_line_indent, last_non_empty_line, found_first_line = 0, BLANK, False
            indents, chars, code = env["indents"], env["chars"], StringIO()
            while env["last_line"] < token.map[-1]:
                line = self.readline(env)
                if line.strip():
                    last_non_empty_line = line
                    current_line_indent = self._get_num_indent(last_non_empty_line)
                    if not found_first_line:  # we can compute the indent constraints
                        if not indents.reference:  # we initialize all the indents
                            indents.reference = indents.trailing = current_line_indent
                        indents.leading = current_line_indent
                        # write to the buffer our noncode as code
                        code.writelines(self.noncode_block(env))
                    found_first_line = True
                code.writelines(line)  # write the line of code to the buffer
            # update the last character state based on the last line.
            vars(chars).update(chars.get_state(last_non_empty_line))
            indents.trailing = current_line_indent  # update the trailing indent state
            return code.getvalue()  # generate a string from the buffer

        def noncode_block(self, env):
            """unquoted markdown -quote-> unindented string -indent-> python block string"""
            indents, chars = env["indents"], env["chars"]
            noncode = not_indented = BLANK
            noncode_indent = self._get_noncode_indent(indents, chars)
            for x in env["noncode_lines"] + [self.NotIndented(BLANK)]:
                if isinstance(x, self.Noncode):
                    noncode += x
                if isinstance(x, self.NotIndented):
                    if chars.quotes:  # indent the code according
                        noncode = indent(noncode, SPACE * noncode_indent)
                    else:  # quote the markdown block
                        noncode = self._get_quoted(noncode, noncode_indent, env)
                    not_indented += noncode  # promote not quoted to not indented
                    # clear the unquoted buffer
                    noncode = BLANK
                    if x.strip():  # add the non empty lines to the unindented block
                        not_indented += SPACE * noncode_indent + x
            env["noncode_lines"].clear()
            return indent(not_indented, SPACE * indents.reference)

        @staticmethod
        def _get_noncode_indent(indents, chars, **_):
            """compute the current indent based on the enclosing blocks"""
            return (
                indents.trailing
                if chars.quotes  # then we require no adjustment
                else max(indents.trailing + 4, indents.leading)
                if chars.colon  # then we want to indent things like docstrings
                else indents.leading
                if indents.leading
                >= indents.trailing  # the leading indent defines the indent
                else indents.trailing  # the trailing indent defines in the indent
            ) - indents.reference  # remove the reference indent

        @staticmethod
        def _get_num_indent(str):
            """get the leading indents of block string"""
            line = StringIO(str).readline()
            return len(line) - len(line.lstrip())

        @staticmethod
        def _get_quoted(input, indent=0, env=None):
            """heuristics that quote a narrative block as a block string."""
            input = dedent(input)
            quote = QUOTES[QUOTES[0] in input]
            l, r = input.lstrip(), input.rstrip().rstrip(CONTINUATION)
            if not (l or r):  # we have a blank string
                return input
            begin, end = input[: len(input) - len(l)], input[len(r) :]
            return (  # recombine all of the parts into quoted python
                begin  # leading whitespace
                + SPACE * indent  # computed indent
                + quote  # enter block string
                + Tangle._get_escaped_string(
                    input[len(input) - len(l) : len(r)], quote[0]
                )  # code body
                + quote  # exit block string
                + env["terminal_character"]  # computed trailing character
                + end  # trailing whitespace
            )

    @staticmethod
    def _get_escaped_string(object, quote='"'):
        from re import subn

        return subn(r"%s{1,1}" % quote, "\\" + quote, object)[0]


def load_ipython_extension(shell):
    from traitlets import Instance

    def tangle(line, cell):
        print(shell.tangle.render(cell))

    def parse(line, cell):
        print(shell.tangle.parse(cell))

    shell.add_traits(tangle=Instance(Tangle, ()))
    shell.input_transformer_manager.cleanup_transforms.insert(
        0, shell.tangle.render_lines
    )
    shell.register_magic_function(tangle, "cell")
    shell.register_magic_function(parse, "cell")


def unload_ipython_extension(shell):
    if shell.has_trait("tangle"):
        shell.input_transformer_manager.cleanup_transforms = list(
            filter(
                shell.tangle.render_lines.__ne__,
                shell.input_transformer_manager.cleanup_transforms,
            )
        )
