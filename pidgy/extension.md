    import pidgy.shell
    
    def load_ipython_extension(shell):

`pidgy` provides an alternative use as an IPython extension; `load_ipython_extension` and `unload_ipython_extension` identify configuration functions to `IPython`.

        shell.add_traits(manager=pidgy.pidgyShell.manager, loaders=pidgy.shell.pidgyShell.loaders, definitions=pidgy.shell.pidgyShell.definitions, weave=pidgy.shell.pidgyShell.weave)
        shell._post_run_cell = types.MethodType(pidgy.shell.pidgyShell._post_run_cell, shell)
        shell._post_exec = types.MethodType(pidgy.shell.pidgyShell._post_exec, shell)
        pidgyShell.init_pidgy(shell)
        shell.input_transformers_post.append(pidgy.tangle.demojize)

        shell.input_transformer_manager = pidgy.shell.pidgyShell.pidgyManager(parent=shell)

<!--  -->

    def unload_ipython_extension(self):
        try:
            self.events.unregister("post_run_cell", self._post_run_cell)
        except ValueError:...
        loader = self.loaders.pop(pidgy.pidgyLoader)
        self.ast_transformers = [x for x in self.ast_transformers if not isinstance(x, (pidgy.tangle.ExtraSyntax, pidgy.testing.Definitions))]
        self.ast_transformers.extend([pidgy.tangle.ExtraSyntax(), pidgy.testing.Definitions()])
        if loader is not None:
            loader.__exit__(None, None, None)