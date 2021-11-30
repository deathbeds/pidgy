"""``pidgy``s approach to converting markdown to python
-------------------------------

``pidgy``s novelty comes from its heuristics for converting markdown into python code.
unlike most literate programming implementations, ``pidgy``s approach relies on indented
code blocks defining a powerful metalanguage that allows markdown and python to cooperate
in a literate documentation.
"""
from textwrap import dedent, indent

from .markdown import Markdown, Renderer
from .models import QUOTES, SPACE

__all__ = ("tangle",)

DOCTEST_CHAR, CONTINUATION_CHAR, COLON_CHAR, QUOTES_CHARS = 62, 92, 58, {39, 34}


class Python(Markdown):
    """a line-for-line markdown to python renderer"""

    def generic(self, env, next=None):
        indents, chars = env["indents"], env["chars"]
        if next is None:
            env["terminal_character"] = ";"

        else:
            if not indents.reference:
                indents.trailing = indents.reference = next.meta["leading"]
            indents.leading = next.meta["leading"]

        noncode_indent = self._get_noncode_indent(indents, chars) - indents.reference
        input = super().generic(env, next)
        if chars.quotes:  # indent the code according
            input = indent(input, SPACE * noncode_indent)
        else:  # quote the markdown block
            input = self._get_quoted(input, noncode_indent, env)
        return indent(input, SPACE * indents.reference)

    def code_block(self, token, options, env):
        indents, chars = env["indents"], env["chars"]
        indents.trailing = token.meta["trailing"]
        chars.colon = token.meta["colon"]
        chars.quotes = token.meta["quotes"]
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
            begin  # leading whitespace
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
