# Extra langauge features of `pidgy`

    def load_ipython_extension(shell):
        ExtraSyntax(shell=shell).register()

<!--

    import IPython, typing as τ, mistune as markdown, IPython, importnb as _import_, textwrap, ast, doctest, typing, re
    import dataclasses, ast, pidgy
    with pidgy.pidgyLoader(lazy=True):
        try: from . import events
        except: import events

-->

## naming variables with gestures.

    def demojize(lines, delimiters=('_', '_')):

We know naming is hard, there is no point focusing on it. `pidgy` allows authors
to use emojis as variables in python. They add extra color and expression to the narrative.

        str = ''.join(lines)
        import tokenize, emoji, stringcase; tokens = []
        try:
            for token in list(tokenize.tokenize(
                __import__('io').BytesIO(str.encode()).readline)):
                if token.type == tokenize.ERRORTOKEN:
                    string = emoji.demojize(token.string, delimiters=delimiters
                                           ).replace('-', '_').replace("’", "_")
                    if tokens and tokens[-1].type == tokenize.NAME: tokens[-1] = tokenize.TokenInfo(tokens[-1].type, tokens[-1].string + string, tokens[-1].start, tokens[-1].end, tokens[-1].line)
                    else: tokens.append(
                        tokenize.TokenInfo(
                            tokenize.NAME, string, token.start, token.end, token.line))
                else: tokens.append(token)
            return tokenize.untokenize(tokens).decode().splitlines(True)
        except BaseException: raise SyntaxError(str)

## Top level return and yield statements.

    class ExtraSyntax(events.Events, ast.NodeTransformer):
        line_transforms = [demojize]
        def visit_FunctionDef(self, node): return node
        visit_AsyncFunctionDef = visit_FunctionDef
        def visit_Return(self, node):
            replace = ast.parse('''__import__('IPython').display.display()''').body[0]
            replace.value.args = node.value.elts if isinstance(node.value, ast.Tuple) else [node.value]
            return ast.copy_location(replace, node)

        def visit_Expr(self, node):
            if isinstance(node.value, (ast.Yield, ast.YieldFrom)):  return ast.copy_location(self.visit_Return(node.value), node)
            return node

        visit_Expression = visit_Expr


    def load_ipython_extension(shell):
        shell.extras = ExtraSyntax(shell=shell).register()

<!--

    def unload_ipython_extension(shell):
        shell.extras.unregister()

-->
