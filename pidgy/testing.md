# Interactive formal testing

Testing is something we added because of the application of notebooks as test units.

A primary use case of notebooks is to test ideas. Typically this in informally using
manual validation to qualify the efficacy of narrative and code. To ensure testable literate documents
we formally test code incrementally during interactive computing.

<!--

    import unittest, doctest, textwrap, dataclasses, IPython, re, pidgy, sys, typing, types, contextlib, ast, inspect
    try: from . import base
    except: import base

-->

    def make_test_suite(*objects: typing.Union[
        unittest.TestCase, types.FunctionType, str
    ], vars, name) -> unittest.TestSuite:

The interactive testing suite execute `doctest and unittest` conventions
for a flexible interface to verifying the computational qualities of literate programs.

        suite, doctest_suite = unittest.TestSuite(), doctest.DocTestSuite()
        suite.addTest(doctest_suite)
        for object in objects:
            if isinstance(object, type) and issubclass(object, unittest.TestCase):
                suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(object))
            elif isinstance(object, str):
                doctest_suite.addTest(doctest.DocTestCase(
                doctest.DocTestParser().get_doctest(object, vars, name, name, 1), doctest.ELLIPSIS))
                doctest_suite.addTest(doctest.DocTestCase(
                InlineDoctestParser().get_doctest(object, vars, name, name, 1), checker=NullOutputCheck))
            elif inspect.isfunction(object):
                suite.addTest(unittest.FunctionTestCase(object))
        return suite

    @base.implementation
    def weave(result):
            shell = IPython.get_ipython()
            globs, filename = shell.user_ns, F"In[{shell.last_execution_result.execution_count}]"

            if not (result.error_before_exec or result.error_in_exec):
                with ipython_compiler(shell):
                    """definitions = [shell.user_ns[x] for x in getattr(shell.measure, 'definitions', [])
                        if x.startswith('test_') or
                        (isinstance(shell.user_ns[x], type)
                         and issubclass(shell.user_ns[x], unittest.TestCase))
                    ]"""
                    definitions = []
                    result = run(make_test_suite(result.info.raw_cell, *definitions, vars=shell.user_ns, name=filename), result)


    def run(suite: unittest.TestCase, cell) -> unittest.TestResult:
            result = unittest.TestResult(); suite.run(result)
            if result.failures:
                msg = '\n'.join(msg for text, msg in result.failures)
                msg = re.sub(re.compile("<ipython-input-[0-9]+-\S+>"), F'In[{cell.execution_count}]', clean_doctest_traceback(msg))
                sys.stderr.writelines((str(result) + '\n' + msg).splitlines(True))
                return result

    @contextlib.contextmanager
    def ipython_compiler(shell):

We'll have to replace how `doctest` compiles code with the `IPython` machinery.

        def compiler(input, filename, symbol, *args, **kwargs):
            nonlocal shell
            return shell.compile(
                ast.Interactive(
                    body=shell.transform_ast(
                    shell.compile.ast_parse(shell.transform_cell(textwrap.indent(input, ' '*4)))
                ).body),
                F"In[{shell.last_execution_result.execution_count}]",
                "single",
            )

        yield setattr(doctest, "compile", compiler)
        doctest.compile = compile

    def clean_doctest_traceback(str, *lines):
        str = re.sub(re.compile("""\n\s+File [\s\S]+, line [0-9]+, in runTest\s+raise[\s\S]+\([\s\S]+\)\n?"""), '\n', str)
        return re.sub(re.compile("Traceback \(most recent call last\):\n"), '', str)

<details><summary>Utilities for the testing module.</summary>
    
    class NullOutputCheck(doctest.OutputChecker):
        def check_output(self, *e): return True

    class InlineDoctestParser(doctest.DocTestParser):
        _EXAMPLE_RE = re.compile(r'`(?P<indent>\s{0})'
    r'(?P<source>[^`].*?)'
    r'`')
        def _parse_example(self, m, name, lineno): return m.group('source'), None, "...", None

</details>

    base.pidgyShell.plugin_manager.register(sys.modules[__name__])
