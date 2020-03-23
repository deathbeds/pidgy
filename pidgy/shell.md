# The `pidgy` literate computing shell

    import ipykernel.kernelapp, traitlets, pidgy, types, pluggy, IPython
    class pidgyShell(ipykernel.zmqshell.ZMQInteractiveShell):

The `pidgy` shell is wrapper around the existing `IPython` shell experience. It explicitly defines the tangle and weave conventions of literate programming to each interactive computing execution. Once the shell is configured, it can be reused as a `jupyter` kernel or `IPython` extension that supports the `pidgy` [Markdown]/[IPython] metalanguage and metasyntax.

## `pidgy` specification

        @pidgy.specification(firstresult=True)
        def tangle(str:str)->str:

The `tangle` step operates on an input string that will become compiled source code. In a literate program, the source is written primarily in the documentation language and tangling converts it to the programming language. In `pidgy`, the tangle steps target valid `IPython` which is a superset of [Python], and requires further processing.

        input_transformers_post = traitlets.List([pidgy.extras.demojize])

`pidgy` includes the ability the use emojis as valid python names through the existing `traitlets` configuration system.

        def transform_cell(self, str: str) -> str:

`IPython` transform cells into blocks of valid [Python], if the source is acceptable. Our `tangle` step is introduced before the `IPython` machinery is triggered. After the cell is transformed, `IPython` expects that [Python] can convert the resulting source code as an [Abstract Syntax Tree], if not we'll receive a `SyntaxError`.

            return super(type(self), self).transform_cell(
                self.manager.hook.tangle(str=str))


        ast_transformers = traitlets.List([pidgy.extras.ExtraSyntax(), pidgy.testing.Definitions()])

Another feature of `IPython` is the ability to intercept [Abstract Syntax Tree]s and change their representation or capture metadata. After these transformations are applied, `IPython` compile the tree into a valid `types.CodeType`.

        @pidgy.specification
        def post_run_cell(result):

The weave step happens after execution, the tangle step happens before. Weaving only occurs if the input is computationally verified. It allows different representations of the input to be displayed. `pidgy` will implement templated Markdown displays of the input and formally test the contents of the input.

        def _post_run_cell(self, result):

A wrapped function that will be called by the IPython post_run_cell event.

            self.manager.hook.post_run_cell(result=result)

        enable_html_pager = traitlets.Bool(True)
        definitions = traitlets.List()
        manager = traitlets.Instance('pluggy.PluginManager', args=('pidgy',))
        loaders = traitlets.Dict()

`pidgy` mixes the standard `IPython` configuration system and its own `pluggy` specification and implementation.

## The `pidgy` specification

        def load_ipython_extension(shell):

The pidgy kernel makes it easy to access the pidgy shell, but it can also be used an IPython extension.

            shell._post_run_cell = types.MethodType(pidgyShell._post_run_cell, shell)
            pidgyShell.init_pidgy(shell)
            shell.transform_cell = types.MethodType(pidgyShell.transform_cell, shell)

<!--  -->

        def unload_ipython_extension(self):
            self.events.unregister("post_run_cell", self._post_run_cell)
            self.events.unregister("post_run_cell", pidgy.weave.post_run_cell)
            loader = self.loaders.pop(pidgy.pidgyLoader)
            if loader is not None:
                loader.__exit__(None, None, None)


        def init_pidgy(self):

Initialize `pidgy` specific behaviors.

            self.manager.add_hookspecs(type(self))
            for object in (
                pidgy.tangle, pidgy.weave, pidgy.testing, pidgy.extras
            ):

The tangle and weave implementations are discussed in other parts of this document. Here we register each of them as `pluggy` hook implementations.

                self.manager.register(object)
            self.events.register("post_run_cell", self._post_run_cell)

            if pidgy.pidgyLoader not in self.loaders:

`pidgy` enters a loader context allowing [Markdown] and notebook files to be used permissively as input.

                self.loaders[pidgy.pidgyLoader] = pidgy.pidgyLoader().__enter__()

It also adds a few extra features to the shell.

            self.user_ns["shell"] = self
            self.user_ns.update({k: v for k, v in vars(IPython.display).items()
                if pidgy.util.istype(v, IPython.core.display.DisplayObject)
            })

and allows json syntax as valid python input.

            pidgyShell.init_json(self)

        def init_json(self):

If Python is put close to a microscope, it supports most `json`s syntax. `pidgy` wants it to be easy
for folks to copy and paste json data into code. We acheive this by modifying the built in settings.

            import builtins
            builtins.yes = builtins.true = True
            builtins.no = builtins.false = False
            builtins.null = None

        def __init__(self, *args, **kwargs):

Override the initialization of the conventional IPython kernel to include the pidgy opinions.

            super().__init__(*args, **kwargs)
            self.init_pidgy()


    load_ipython_extension = pidgyShell.load_ipython_extension
    unload_ipython_extension = pidgyShell.unload_ipython_extension
