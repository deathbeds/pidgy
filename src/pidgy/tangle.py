"""tangle.py provides the Markdown to Python translation model.
"""
from textwrap import dedent, indent

from .markdown import Markdown, Renderer
from .models import QUOTES, SPACE

__all__ = ("tangle",)

DOCTEST_CHAR, CONTINUATION_CHAR, COLON_CHAR, QUOTES_CHARS = 62, 92, 58, {39, 34}

# an instance of this class is used to transform markdown to valid python
# in the ipython extension. the python conversion is constrained by being
# a line for line transformation using indent code blocks (not code fences)
# as references for translating the markdown to valid python objects.

# the choice of indented code over code fences allows for more implicit interleaving
# of code and narrative.
class Python(Markdown):
    """a line-for-line markdown to python renderer"""

    markdown_is_block_string = True
    docstring_block_string = True

    def indent(self, input, i=0, prefix=""):
        """indent an input"""
        return indent(input, SPACE * i + prefix)

    def quote(self, input, env, i=0):
        """quote a string which requires the environment state"""
        return self._get_quoted(input, i, env)

    def comment(self, input, i=0):
        """comment an input"""

        return self.indent(input, i, "# ")

    def get_noncode_indent(self, env):
        return (
            self._get_noncode_indent(env["indents"], env["chars"])
            - env["indents"].reference
        )

    # this method is defined by the reusable markdown parent
    def generic(self, env, next=None):
        """process a generic block of markdown text."""

        indents, chars = env["indents"], env["chars"]
        if next is None:
            env["terminal_character"] = ";"

        else:
            if not indents.reference:
                indents.trailing = indents.reference = next.meta["leading"]
            indents.leading = next.meta["leading"]

        input, indent = super().generic(env, next), self.get_noncode_indent(env)

        if chars.quotes:
            # when we find quotes in code around a markdown block we don't augment the string.
            input = self.indent(input, indent)
        elif self.markdown_is_block_string:
            # augment a non-code markdown block as quoted string
            input = self.quote(input, env, indent)
        else:
            input = self.comment(input, indent)

        return self.indent(input, indents.reference)

    def code_block(self, token, options, env):
        """update the state block when code is found."""
        indents, chars = env["indents"], env["chars"]

        # update the trailing indent
        indents.trailing = token.meta["trailing"]

        # measure if there is a preceding colon indicating a python block indent
        chars.colon = token.meta["colon"]

        # measure if triple quotes exist around the surround code block
        chars.quotes = token.meta["quotes"]

        # read the lines pertaining to the raw code.
        return self.readlines(token.map[1], env)

    def render(self, tokens, options, env):
        return dedent(super().render(tokens, options, env))

    @staticmethod
    def _get_noncode_indent(indents, chars, **_):
        """compute the current indent based on the enclosing blocks"""
        if chars.quotes:  # then we require no adjustment
            return indents.reference
        elif chars.colon:
            return max(indents.trailing + 4, indents.leading)
        elif indents.leading >= indents.trailing:
            return indents.leading
        return indents.trailing

    @staticmethod
    def _get_quoted(input, indent=0, env=None):
        """heuristics that quote a non-code block as a string."""
        from .utils import get_escaped_string

        input = dedent(input)
        quote = QUOTES[QUOTES[0] in input]
        l, r = input.lstrip(), input.rstrip()
        if not (l or r):  # we have a blank string
            return input
        begin, end = input[: len(input) - len(l)], input[len(r) :]
        return (  # recombine all of the parts into quoted python
            begin  # leading whitespace1
            + SPACE * indent  # computed indent
            + quote  # enter block string
            + get_escaped_string(
                input[len(input) - len(l) : len(r)], quote[0]
            )  # code body
            + quote  # exit block string
            + env["terminal_character"]  # computed trailing character
            + end  # trailing whitespace
        )


def load_ipython_extension(shell):
    from traitlets import Instance

    def tangle(line, cell):
        print(shell.tangle.render(cell))

    def parse(line, cell):
        print(shell.tangle.parse(cell))

    shell.add_traits(tangle=Instance(Renderer, (), kw=dict(renderer_cls=Python)))
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
