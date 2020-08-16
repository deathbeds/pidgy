# Interactive formal testing

Testing is something we added because of the application of notebooks as test units.

A primary use case of notebooks is to test ideas. Typically this in informally using
manual validation to qualify the efficacy of narrative and code. To ensure testable literate documents
we formally test code incrementally during interactive computing.

    import pidgy.base, traitlets, ast, unittest, IPython, sys
    with pidgy.pidgyLoader(lazy=True):
        import pidgy.compat.unittesting, pidgy.compat.typin

    class Testing(pidgy.base.Trait, pidgy.compat.unittesting.TestingBase):
        medial_test_definitions = traitlets.List()
        pattern = traitlets.Unicode('test_')
        visitor = traitlets.Instance('ast.NodeTransformer')
        results = traitlets.List()
        trace = traitlets.Any()
        update = traitlets.Bool(True)

        @traitlets.default('trace')
        def _default_trace(self):
            return pidgy.compat.typin.InteractiveTyping(parent=self)

        @traitlets.default('visitor')
        def _default_visitor(self):
            return pidgy.compat.unittesting.Definitions(parent=self)

        def post_run_cell(self, result):
            if not self.enabled: return
            if not (result.error_before_exec or result.error_in_exec):
                tests = []
                while self.medial_test_definitions:
                    name = self.medial_test_definitions.pop(0)
                    object = self.parent.user_ns.get(name, None)
                    if name.startswith(self.pattern) or pidgy.util.istype(object, unittest.TestCase):
                        tests.append(object)

                test = pidgy.compat.unittesting.Test(result=result, parent=self.parent, vars=True)
                if self.trace.enabled:
                    with self.trace: test.test(*tests)
                else: test.test()
                if test.test_result.testsRun:
                    IPython.display.display(test)
                    self.results = [
                           x for x in self.results if x._display and x._display.display_id != test._display.display_id
                    ] + [test]


        def stub(self):
            return self.trace.stub()
        def post_execute(self):
            if self.update: 
                for test in self.results:
                    if self.trace.enabled:
                        with self.trace: test.test()
                    else: test.test()
                    test.update()
