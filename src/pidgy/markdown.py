from io import StringIO

from markdown_it import MarkdownIt
from markdown_it.renderer import RendererProtocol

from .models import (
    CELL_MAGIC,
    COLON_CHAR,
    CONTINUATION_CHAR,
    DOCTEST_CHAR,
    QUOTES_CHARS,
    Env,
)


def doctest(state, startLine, end, silent=False):
    """a markdown-it-py plugin for doctests

    doctest are a literate programming convention in python that we
    include in the pidgy grammar. this avoids a mixing python and doctest
    code together."""
    start = state.bMarks[startLine] + state.tShift[startLine]

    if all(map(DOCTEST_CHAR.__eq__, state.srcCharCode[start : start + 3])):
        indent, next = state.bMarks[startLine], startLine + 1
        while next < end:
            if state.isEmpty(next):
                break
            if state.bMarks[next] < indent:
                break
            next += 1
        state.line = next
        token = state.push("doctest", "code", 0)
        token.content = state.getLines(startLine, next, 0, True)
        token.map = [startLine, state.line]
        return True
    return False


def code(state, start, end, silent=False):
    if state.sCount[start] - state.blkIndent >= 4:
        leading, next, quoted, colon = 0, start, False, False
        while next < end:
            if state.isEmpty(next):
                next += 1
                continue
            here = state.bMarks[next] + state.tShift[next]
            if all(map(DOCTEST_CHAR.__eq__, state.srcCharCode[here : here + 3])):
                break
            elif state.sCount[next] - state.blkIndent >= 4:
                if not leading:
                    leading = state.sCount[next]
                trailing = state.sCount[next]
                last_char = state.eMarks[next] - 1
                continued = state.srcCharCode[last_char] == CONTINUATION_CHAR
                length = state.eMarks[next] - (state.bMarks[next] + state.tShift[next])
                if continued:
                    last_char -= 1
                if continued and quoted and length == 1:
                    pass
                else:
                    colon = state.srcCharCode[last_char] == COLON_CHAR
                    quoted = state.srcCharCode[last_char] in QUOTES_CHARS
                    if quoted:
                        quoted = (
                            state.srcCharCode[last_char - 2 : last_char]
                            == (state.srcCharCode[last_char],) * 2
                        )
                    else:
                        quoted = False
                next = last = next + 1
            else:
                break
        state.line = last
        token = state.push("code_block", "code", 0)
        token.content = state.getLines(start, last, 4 + state.blkIndent, True)
        token.map = [start, state.line]
        token.meta.update(
            leading=leading,
            trailing=trailing,
            continued=continued,
            colon=colon,
            quotes=quoted,
        )
        return True
    return False


class Renderer(MarkdownIt):
    def __init__(self, *args, **kwargs):
        args = args or ("gfm-like",)
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


class Markdown(RendererProtocol):
    def generic(self, env, next=None):
        return (
            "".join(env["source"]) if next is None else self.readlines(next.map[0], env)
        )

    def walk(self, tokens, options, env):
        for token in tokens:
            if hasattr(self, token.type):
                yield self.generic(env, token)
                yield getattr(self, token.type)(token, options, env)
        else:
            yield self.generic(env)

    def render(self, tokens, options, env):
        body = StringIO()
        for block in self.walk(tokens, options, env):
            body.writelines(block)
        return body.getvalue()

    def readline(self, env):
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
