# The `pidgy` literate computing shell

    import ipykernel.kernelapp, traitlets, pidgy

    class pidgyShell(ipykernel.zmqshell.ZMQInteractiveShell):

        def transform_cell(self, str: str) -> str:
            return super().transform_cell(pidgy.tangle.tangle(text=str))

        ast_transformers = traitlets.List([pidgy.extras.ExtraSyntax()]).tag(config=True)
        input_transformers_post = traitlets.List([pidgy.extras.demojize])

        def init_json(self):
            import builtins
            builtins.yes = builtins.true = True
            builtins.no = builtins.false = False
            builtins.null = None

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.init_pidgy(), self.init_json()

        def init_pidgy(self):
            self.events.register("post_run_cell", pidgy.testing.post_run_cell)
            self.events.register("post_run_cell", pidgy.weave.post_run_cell)

            self.user_ns["shell"] = self
            pidgy.pidgyLoader().__enter__()

        enable_html_pager = traitlets.Bool(True)
