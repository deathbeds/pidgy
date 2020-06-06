# Interactive formal testing

Testing is something we added because of the application of notebooks as test units.

A primary use case of notebooks is to test ideas. Typically this in informally using
manual validation to qualify the efficacy of narrative and code. To ensure testable literate documents
we formally test code incrementally during interactive computing.

    import pidgy.base, traitlets, ast, unittest, IPython
    with pidgy.pidgyLoader(): import pidgy.compat.unittesting


    class Definitions(ast.NodeTransformer):
        def visit_FunctionDef(self, node):
            shell = IPython.get_ipython()
            shell and shell.definitions.append(node.name)
            return node
        visit_ClassDef = visit_FunctionDef

    def run(suite: unittest.TestCase, cell) -> unittest.TestResult:
            result = unittest.TestResult(); suite.run(result)
            if result.failures:
                msg = '\n'.join(msg for text, msg in result.failures)
                msg = re.sub(re.compile("<ipython-input-[0-9]+-\S+>"), F'In[{cell.execution_count}]', pidgy.util.clean_doctest_traceback(msg))
                sys.stderr.writelines((str(result) + '\n' + msg).splitlines(True))
                return result


    class Testing(pidgy.base.Trait, pidgy.compat.unittesting.TestingBase):
        medial_test_definitions = traitlets.List()
        pattern = traitlets.Unicode('test_')
        visitor = traitlets.Instance('ast.NodeTransformer')

        @traitlets.default('visitor')
        def _default_visitor(self): return pidgy.compat.unittesting.Definitions(parent=self)

        @pidgy.implementation
        def post_run_cell(self, result):
            if not (result.error_before_exec or result.error_in_exec):
                tests = []
                with pidgy.compat.unittesting.ipython_compiler(self.parent):
                    while self.medial_test_definitions:
                        name = self.medial_test_definitions.pop(0)
                        object = self.parent.user_ns.get(name, None)
                        if name.startswith(self.pattern) or pidgy.util.istype(object, unittest.TestCase):
                            tests.append(object)
                    self.test(result, *tests)
