# Interactive formal testing

Testing is something we added because of the application of notebooks as test units.

A primary use case of notebooks is to test ideas. Typically this in informally using
manual validation to qualify the efficacy of narrative and code. To ensure testable literate documents
we formally test code incrementally during interactive computing.

    import pidgy.base, traitlets, ast, unittest, IPython
    with pidgy.pidgyLoader(lazy=True): import pidgy.compat.unittesting

    class Testing(pidgy.base.Trait, pidgy.compat.unittesting.TestingBase):
        medial_test_definitions = traitlets.List()
        pattern = traitlets.Unicode('test_')
        visitor = traitlets.Instance('ast.NodeTransformer')
        results = traitlets.List()

        @traitlets.default('visitor')
        def _default_visitor(self):
            return pidgy.compat.unittesting.Definitions(parent=self)

        def post_run_cell(self, result):
            if not (result.error_before_exec or result.error_in_exec):
                tests = []
                while self.medial_test_definitions:
                    name = self.medial_test_definitions.pop(0)
                    object = self.parent.user_ns.get(name, None)
                    if name.startswith(self.pattern) or pidgy.util.istype(object, unittest.TestCase):
                        tests.append(object)

                test = pidgy.compat.unittesting.Test(result=result, parent=self.parent, vars=True)
                with pidgy.compat.unittesting.ipython_compiler(self.parent): test.test(*tests)
                if test.test_result.testsRun:
                    IPython.display.display(test)
                    self.results = [
                           x for x in self.results if x._display and x._display.display_id != test._display.display_id
                    ] + [test]



        def post_execute(self):
            for test in self.results:
                test.test()
                test.update()
