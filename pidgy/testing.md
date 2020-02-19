    import IPython as python, doctest, textwrap, dataclasses, IPython, re
    pidgy= None

In literate programs, `"code"` is deeply entangled with the narrative.
`"code"` objects can signify meaning, with enriched veracity 
through formal software testing.
`python` introduced the `doctest` literate programming convention that indicates some text in a narrative can be tested.
`pidgy` extends the `doctest` opinion to the inline markdown code.
Each time a `pidgy` cell is executed, the `doctest`s and inline code are executed ensuring that
any code in a `pidgy` program is valid.

    @dataclasses.dataclass
    class Testing:
        shell: object = dataclasses.field(default_factory=IPython.get_ipython)
        cell_unit_tests: list = dataclasses.field(default_factory=list)
        def post_run_cell(self, result):
            if not(result.error_before_exec or result.error_in_exec):
                result.runner = test_markdown_string(result.info.raw_cell, IPython.get_ipython(), False, doctest.ELLIPSIS)

    def load_ipython_extension(shell): 
        unload_ipython_extension(shell)
        shell.testing = Testing(shell=shell)
        shell.ast_transformers.append(TestingNodes(shell=shell))
        shell.events.register('post_run_cell', shell.testing.post_run_cell)


    import doctest, contextlib, mistune as markdown, re, ast, __main__, IPython, operator
    shell = IPython.get_ipython()

`test_markdown_string` extends the standard python `doctest` tools 
to inline code objects written in markdown.  
This approach compliments are markdown forward programming language to test
intertextual references between code and narrative.


    INLINE = re.compile(
        markdown.InlineGrammar.code
        .pattern[1:]
        .replace('[\s\S]*', '?P<source>[\s\S]+')
        .replace('+)\s*', '{1,2})(?P<indent>\s{0})'), 
    )
    INLINE = re.compile("""`{1}(
        ?P<indent>\s{0})(?P<source>[^`\n\r]+
    )`{1}""")
    (TICK,), SPACE = '`'.split(), ' '

    def test_markdown_string(str, shell=shell, verbose=False, compileflags=None):
        globs, filename = shell.user_ns, F"In[{shell.last_execution_result.execution_count}]"
        runner = doctest.DocTestRunner(verbose=verbose, optionflags=compileflags)  
        parsers = DocTestParser(runner), InlineDoctestParser(runner)
        parsers = {
            parser: doctest.DocTestFinder(verbose, parser).find(str, filename) for parser in parsers
        }
        examples = sum([test.examples for x in parsers.values() for test in x], [])
        examples.sort(key=operator.attrgetter('lineno'))
        with ipython_compiler(shell):
            for example in examples:
                for parser, value in parsers.items():
                    for value in value:
                        if example in value.examples:
                            with parser:
                                runner.run(doctest.DocTest(
                                    [example], globs, value.name, filename, example.lineno, value.docstring
                                ), compileflags=compileflags, clear_globs=False)
                if hasattr(shell.testing, 'unit_cell_tests'):
                    while shell.testing.unit_cell_tests:
                        shell.testing.unit_cell_tests.pop()
        shell.log.info(F"In[{shell.last_execution_result.execution_count}]: {runner.summarize()}")
        return runner


    class DocTestParser(doctest.DocTestParser):
        _checkers = []
        def __init__(self, runner): self.runner = runner
        def __enter__(self):
            self._checkers.append(self.runner._checker)
            self.runner._checker = getattr(self, '_checker', doctest.OutputChecker)()
        def __exit__(self, *e):
            self.runner._checker = self._checkers.pop(-1)

        def _parse_example(self, m, name, lineno):
            self.m = m
            return super()._parse_example(m, name, lineno)

    class NullOutputCheck(doctest.OutputChecker):
        def check_output(self, *e): return True

    class InlineDoctestParser(DocTestParser):
        _checker = NullOutputCheck
        _EXAMPLE_RE = INLINE
        def _parse_example(self, m, name, lineno):
            return m.group('source'), None, "...", None

    @contextlib.contextmanager
    def ipython_compiler(shell):
        def compiler(input, filename, symbol, *args, **kwargs):
            nonlocal shell
            return shell.compile(
                ast.Interactive(
                    body=shell.transform_ast(
                        shell.compile.ast_parse(shell.transform_cell(textwrap.indent(input, ' '*4)))
                    ).body
                ),
                F"In[{shell.last_execution_result.execution_count}]",
                "single",
            )

        yield setattr(doctest, "compile", compiler)
        doctest.compile = compile



    def unload_ipython_extension(shell): 
        try: 
            shell.events.unregister('post_run_cell', shell.testing.post_run_cell)
        except: ...



    function_unit_test = re.compile('test_[a-z|A-Z]+')
    class_unit_test = re.compile('Test[A-Z]+')

    @dataclasses.dataclass
    class TestingNodes(__import__('ast').NodeTransformer):
        shell: object = dataclasses.field(default_factory=IPython.get_ipython)
        def FunctionDef(self, node):
            if function_unit_test.match(node.name):
                self.shell.testing.cell_unit_tests.append(node.name)
            return node

        def visit_ClassDef(self, node):
            if class_unit_test.match(node.name): self.shell.testing.cell_unit_tests.append(node.name)
            return node
