# The `pidgy` literate computing shell

Did y'all know that the `IPython` is a configurable object? That we can modify the heck out it. `pidgy` uses liberally uses `IPython`s configurable Read-Eval-Print-Loop machinery to craft a bespoke literate computing experience.

    import ipykernel.kernelapp, traitlets, pidgy, types

    class pidgyShell(ipykernel.zmqshell.ZMQInteractiveShell):

Primarly, the `pidgyShell` formalizes the tangle and weave steps of literate programming with each execution of code.

        def transform_cell(self, str: str) -> str:

The tangle step occurs before any compite happens. It takes an input string and converts it a valid programming language, in out case valid `IPython`.

            str = pidgy.tangle.tangle(str)
            return super(type(self), self).transform_cell(str)

### Extra language features

After the tangle, step `pidgy` uses existing `IPython` machinery to tangle two other opinionated language features:

1. `emoji` for [Python] variables names.
2. top-level return and yield statements.

Emojis are not valid variables names in [Python], but `pidgy` they are. Emojis represent gestures that can ease the challenge with naming, and using visual symbols instead.

        input_transformers_post = traitlets.List([pidgy.extras.demojize])

`IPython` introduces top-level `"await"` statements, `pidgy` builds of this concept to expose
`"return" and "yeild"` statements at the top-level.

        ast_transformers = traitlets.List([pidgy.extras.ExtraSyntax()]).tag(config=True)

<!--  -->

        def init_json(self):

If Python is put close to a microscope, it supports most `json`s syntax. `pidgy` wants it to be easy
for folks to copy and paste json data into code. We acheive this by modifying the built in settings.

            import builtins
            builtins.yes = builtins.true = True
            builtins.no = builtins.false = False
            builtins.null = None

<!--  -->

        def init_weave(self):

The weave step is trigger after the code is code is executed. Weaving triggers alternate representations of the source. In `pidgy` we add explicit markdown rendering with jinja templates and formal testing of the source.

            self.events.register("post_run_cell", pidgy.testing.post_run_cell)
            self.events.register("post_run_cell", pidgy.weave.post_run_cell)
            self.loaders = getattr(self, 'loaders', {})
            if pidgy.pidgyLoader not in self.loaders:
                self.loaders[pidgy.pidgyLoader] = pidgy.pidgyLoader().__enter__()

<!--  -->

        def load_ipython_extension(shell):

The pidgy kernel makes it easy to access the pidgy shell, but it can also be used an IPython extension.

            pidgyShell.init_weave(shell)
            pidgyShell.init_json(shell)
            shell.transform_cell = types.MethodType(pidgyShell.transform_cell, shell)

<!--  -->

        def unload_ipython_extension(self):
            self.events.unregister("post_run_cell", pidgy.testing.post_run_cell)
            self.events.unregister("post_run_cell", pidgy.weave.post_run_cell)
            loader = self.loaders.pop(pidgy.pidgyLoader)
            if loader is not None:
                loader.__exit__(None, None, None)

        enable_html_pager = traitlets.Bool(True)

<!--  -->

        def __init__(self, *args, **kwargs):

Override the initialization of the conventional IPython kernel to include the pidgy opinions.

            super().__init__(*args, **kwargs)
            self.init_weave(), self.init_json()
            self.user_ns["shell"] = self



    load_ipython_extension = pidgyShell.load_ipython_extension
    unload_ipython_extension = pidgyShell.unload_ipython_extension
