import ast
import collections
import contextlib
import doctest
import functools
import inspect
import io
import itertools
import textwrap
import unittest

import IPython
import traitlets

from . import get_ipython


class AstProfile(ast.NodeTransformer):
    """pluck metadata from the ast for use by the pidgy extension"""

    def __init__(self):
        self.data = collections.defaultdict(list)
        self._depth = 0

    def __enter__(self):
        if not self._depth:
            self.data.clear()
        self._depth += 1

    def __exit__(self, *e):
        self._depth -= 1

    def visit(self, node):
        with self:
            return super().visit(node)

    def capture(self, node):
        self.data[type(node)].append(node)
        return node

    visit_FunctionDef = visit_ClassDef = capture


@functools.singledispatch
def get_test(object):
    """create a test case from the object, return None if no test"""
    if inspect.isfunction(object):
        return unittest.FunctionTestCase(object)
    return


@get_test.register
def get_test_ast(object: ast.AST):
    if object.name in get_ipython().user_ns:
        return get_test(get_ipython().user_ns[object.name])


@get_test.register
def get_test_str(object: str):
    vars = get_ipython().user_ns
    name = get_ipython().user_module.__name__
    doctest_suite = doctest.DocTestSuite()
    test_case = doctest.DocTestParser().get_doctest(object, vars, name, name, 1)
    test_case.examples and doctest_suite.addTest(
        doctest.DocTestCase(test_case, doctest.ELLIPSIS)
    )
    if doctest_suite._tests:
        return doctest_suite


@get_test.register
def get_test_case(object: type):
    if issubclass(object, unittest.TestCase):
        return unittest.defaultTestLoader.loadTestsFromTestCase(object)


@functools.singledispatch
def get_test_object(x):
    """return the python object being tested"""
    return


@get_test_object.register
def get_test_object_str(x: str):
    if any(doctest.DocTestParser._EXAMPLE_RE.finditer(x)):
        return x


@get_test_object.register
def get_test_object_ast(x: ast.AST):
    if isinstance(x, ast.FunctionDef):
        if x.name.startswith("test_"):
            return x
    if isinstance(x, ast.ClassDef):
        return x


def get_test_objects(*x):
    return list(filter(bool, map(get_test_object, x)))


def get_formatted_results(result):
    import emoji

    body = io.StringIO()
    if result is not None:
        if result.testsRun:
            if result.errors:
                body.writelines("\n".join(msg for text, msg in result.errors))

            if result.failures:
                body.writelines("\n".join(msg for text, msg in result.failures))

        body = body.getvalue()

        return f"""```pytb\n{emoji.emojize(body, use_aliases=True)}\n```"""
    return "✔"


@contextlib.contextmanager
def ipython_compiler(shell):
    def compiler(input, filename, symbol, *args, **kwargs):
        return get_ipython().compile(
            ast.Interactive(
                body=shell.transform_ast(
                    shell.compile.ast_parse(
                        shell.transform_cell(textwrap.indent(input, " " * 4))
                    )
                ).body
            ),
            f"In[{shell.last_execution_result.execution_count}]",
            "single",
        )

    yield setattr(doctest, "compile", compiler)
    doctest.compile = compile


def collect_tests(*object):
    suite = unittest.TestSuite()
    for x in object:
        y = get_test(x)
        if y:
            yield y
    suite.addTests(filter(bool, map(get_test, object)))
    if suite._tests:
        return suite


def collect(*object):
    suite = unittest.TestSuite()
    suite.addTests(filter(bool, map(get_test, object)))
    if suite._tests:
        return suite


def run(suite):
    if suite:
        with ipython_compiler(get_ipython()):
            result = unittest.TestResult()
            suite.run(result)
        return result


def get_markdown_test_results(objects):
    return IPython.display.Markdown(get_formatted_results(run(collect(*objects))))


def post_run_cell(result):
    objects = get_test_objects(
        result.info.raw_cell,
        *itertools.chain(*get_ipython().ast_profiler.data.values()),
    )

    if objects:
        id = get_ipython().id
        tests = get_ipython().displays_manager.tests
        if id in tests:
            tests[id] = tests[id][0], objects
        else:
            tests[id] = IPython.display.DisplayHandle(), objects
        tests[id][0].display(get_markdown_test_results(objects))

    for id, (display, objects) in get_ipython().displays_manager.tests.items():
        if id == get_ipython().id:
            continue
        display.update(get_markdown_test_results(objects))


def load_ipython_extension(shell):
    shell.add_traits(ast_profiler=traitlets.Instance(AstProfile, args=()))
    shell.ast_transformers.append(shell.ast_profiler)
    shell.events.register(post_run_cell.__name__, post_run_cell)


def unload_ipython_extension(shell):
    shell.ast_transformers = [
        x for x in shell.ast_transformers if not isinstance(x, AstProfile)
    ]
    shell.events.unregister(post_run_cell.__name__, post_run_cell)
