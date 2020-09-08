    import pidgy.shell, types
    
    def load_ipython_extension(shell):

`pidgy` provides an alternative use as an IPython extension; `load_ipython_extension` and `unload_ipython_extension` identify configuration functions to `IPython`.

        shell.add_traits(weave=pidgy.shell.pidgyShell.weave, testing=pidgy.shell.pidgyShell.testing, loaders=pidgy.shell.pidgyShell.loaders)
        pidgy.shell.pidgyShell.init_pidgy(shell)
        shell.input_transformers_post.append(pidgy.tangle.demojize)

        shell.input_transformer_manager = pidgy.shell.pidgyShell._default_tangle(shell)

<!--  -->

    def unload_ipython_extension(shell):
    
        for key in "input_transform_manager weave testing".split():
             if hasattr(shell, key):
                 object = getattr(shell, key)
                 object.enabled = False
                 for x in object.register_keys:
                     if hasattr(object, x):
                         shell.events.unregister(x, getattr(object, x))
        shell.ast_transformers = [x for x in shell.ast_transformers if not isinstance(x, (pidgy.tangle.ExtraSyntax,))]
        