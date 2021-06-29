"""a line for line markdown to python tangle

tangle is the step in literate programming where the document language is
translated to the programming language. in this module, we have a null transformer
and a `pidgy`'s custom heuristics for translating markdown to python.
"""
import ast
import functools
import io
import itertools
import re
import textwrap

import markdown_it
import mdit_py_plugins

from pidgy.lisp import HY_MATCH


def get_num_indent(str):
    """get the leading indents of block string"""
    line = io.StringIO(str).readline()
    return len(line) - len(line.lstrip())


QUOTES = "'''", '"""'


class Unindented(str):
    pass


class Unquoted(str):
    pass


def get_quoted(str, indent=0, trailing="", fence=False):
    """heuristics that quote a narrative block as valid python."""
    str = textwrap.dedent(str)
    quote = QUOTES[QUOTES[0] in str]
    quote, l, r = QUOTES[QUOTES[0] in str], str.lstrip(), str.rstrip().rstrip("\\")

    if not (l or r):
        # this represents the case of a blank string
        return str
    # concatenate all the strings pieces together in the correct order
    # ending with a quoted block of python
    return (
        str[: len(str) - len(l)]
        + " " * indent
        + "r"  # experimental, but i think regular strings make sense
        + quote
        + str[len(str) - len(l) : len(r)]
        + quote
        + trailing
        + str[len(r) :]
    )


class Null(markdown_it.renderer.RendererProtocol):
    def render(self, tokens, options, env):
        return "".join(env["source"])


class Python(markdown_it.renderer.RendererProtocol):
    """a markdown to python renderer"""

    def init_env(self, env):
        # as we move through the lines we keep track of the indent
        # as reference for including noncode
        env.setdefault("last_indent", 0)

        # is the code block in a fence
        env.setdefault("in_fence", False)

        # does the code block end with a colon indicating a new block
        env.setdefault("ends_with_colon", False)

        # does the code block end with a line continuation?
        env.setdefault("ends_with_continuation", False)

        # does the code block explicitly define quotes?
        env.setdefault("ends_with_quotes", False)

        # at the end of a block we need to a semincolon to suppress output.
        # this flag is needed for the last token
        env.setdefault("trailing_character", "")

    __init__ = markdown_it.renderer.RendererHTML.__init__

    def flush(self, env):
        unquoted = unindented = ""

        indent = self.compute_indent(env)
        for x in env["unprocessed"] + [Unindented("")]:
            if isinstance(x, Unquoted):
                unquoted += x
            if isinstance(x, Unindented):
                if env["ends_with_quotes"]:
                    unquoted = textwrap.indent(unquoted, " " * indent)
                else:
                    unquoted = get_quoted(unquoted, indent, env["trailing_character"])
                unindented += unquoted
                unquoted = ""
                if x.strip():
                    unindented += " " * indent + x

        env["unprocessed"].clear()
        unindented = self.continuation(unindented, env, indent)
        return textwrap.indent(unindented, " " * env.get("reference_indent", 0))

    def compute_indent(self, env):
        if env["ends_with_quotes"]:
            # explicit quotes require no adjustements
            indent = env["last_indent"]
        elif env["ends_with_colon"]:
            indent = max(env["last_indent"] + 4, env.get("next_indent", 0))
        else:
            indent = env[
                ["last_indent", "next_indent"][
                    env.get("next_indent", 0) >= env["last_indent"]
                ]
            ]
        indent -= env["reference_indent"]
        return indent

    def fence(self, token, options, env):
        """render a code fence, if and of if there is info."""
        if not token.info:
            env["in_fence"] = True
            try:
                line = env["ends_with_continuation"] and "\\" or ""
                env["unprocessed"].append(Unquoted(self.readline(env).replace("`", "")))
                return self.code_block(token, options, env)
            finally:
                env["in_fence"] = False
                line = env["ends_with_continuation"] and "\\" or ""
                env["unprocessed"].append(Unquoted(self.readline(env).replace("`", "")))

        # it would be cool to do special things on the language
        # pidgy is refusing to make opinions here because they'll never stop.

    def continuation(self, str, env, indent):
        """attach python line continuations where needed"""

        # prepend leading continuations to the block
        if env["ends_with_continuation"]:
            body = io.StringIO()
            for line in str.splitlines(True):
                if line.strip():
                    env["ends_with_continuation"] = False
                if env["ends_with_continuation"]:
                    line = " " * indent + "\\" + line
                body.writelines(line)

            str = body.getvalue()

        # append trailing continuations to the block
        r = str.rstrip()
        env["ends_with_continuation"] = r.endswith("\\")
        if env["ends_with_continuation"]:
            return r + "".join(
                " " * indent + "\\" + x if i else x
                for i, x in enumerate(str[len(r) :].splitlines(True))
            )
        return str

    def code_block(self, token, options, env):
        """render a code block"""
        code = io.StringIO()
        map = token.map

        if env["in_fence"]:
            # shrink the map for fences to exclude the ticks
            map = map[0] + 1, map[1] - 1

        env.pop("next_indent", None)
        last_indent = 0
        # process the code lines to know what happens AFTER the noncode
        while env["last_line"] < map[-1]:
            line = self.readline(env)
            blank = len(list(itertools.takewhile(" >".__contains__, line)))
            line = " " * blank + line[blank:]

            if line.strip():
                if env["in_fence"]:
                    line = textwrap.indent(line, " " * 4)

                last_indent = get_num_indent(line)

                if "next_indent" not in env:
                    env["next_indent"] = last_indent

                if "reference_indent" not in env:
                    env["reference_indent"] = last_indent

            code.writelines(line)

        # buffer to string
        code = code.getvalue()


        # combine the front_matter block (it can only be nonempty at most one time), noncode and code into a python block
        noncode = self.flush(env)

        self.push_env(code, env)
        
        env["last_indent"] = last_indent
        # update the environment state
        
        
        return noncode + code

    def push_env(self, code, env):
        """update the rendered environment based on the codes trailing characters"""
        end = code.rstrip()

        # does the code end with a python line continuation
        env["ends_with_continuation"] = end.endswith("\\")

        # does the code with a python block statement
        env["ends_with_colon"] = end.endswith(":")

        end = end.rstrip("\\")
        # does the code end with explicit block quotations
        env["ends_with_quotes"] = end.endswith(QUOTES)

    def front_matter(self, token, options, env):
        """manually create a blob of code that can import the matter in the local namespace"""
        if token.markup == "---":
            loader = "yaml.safe_load"
        if token.markup == "+++":
            loader = "toml.load"
        self.readline(env)
        content = self.readlines(token.map[-1] - 1, env)
        self.readline(env)
        env["unprocessed"].append(
            Unindented(
                f"""locals().update(__import__("{loader}")({QUOTES[0]}\n{content}{QUOTES[0]})))
"""
            )
        )

    def readline(self, env):
        try:
            return env["source"].readline()
        finally:
            env["last_line"] += 1

    def readlines(self, stop, env):
        str = """"""
        while env["last_line"] < stop:
            str += self.readline(env)
        return str

    def render(self, tokens, options, env):
        """render the markdown tokens in a blob of python code."""
        body = io.StringIO()

        # set the initial state for the render
        self.init_env(env)

        for token in tokens:
            # walk the tokens and only act if the type name is in the class
            if hasattr(self, token.type):
                env["unprocessed"].append(Unquoted(self.readlines(token.map[0], env)))
                body.writelines(getattr(self, token.type)(token, options, env) or "")

        # after this we need hide outputs
        env["trailing_character"] = ";"

        # make sure a reference indent is set in case there was no code block found
        env.setdefault("reference_indent", 4)

        # make sure a reference indent is set in case there was no code block found
        env["next_indent"] = env["last_indent"] = env["reference_indent"]

        # clear the source unquoted with a noncode block
        env["unprocessed"].append(Unquoted(self.readlines(10000, env)))
        body = body.getvalue() + self.flush(env)
        return textwrap.dedent(body)

    def reference(self, token, options, env):
        env["unprocessed"].append(
            Unindented(
                f"""locals().setdefault("__annotations__", dict()).setdefault("{token.meta["name"]}", __import__("IPython").display.Markdown("[{token.meta["name"]}]({token.meta["href"]} "{token.meta["title"]}")"))
"""
            )
        )
        self.readlines(token.map[-1], env)
