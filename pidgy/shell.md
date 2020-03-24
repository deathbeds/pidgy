# The `pidgy` literate computing shell

A powerful feature of the `jupyter` ecosystem is a generalized implementation of the [Shell] & [Kernel] model for interactive computing in interfaces like the terminal and notebooks. That is to say that different programming languages can use the same interfaces, `jupyter` supports [over 100 languages now][kernel languages]. The general ability to support different languages is possible because of configurable interfaces for the `IPython.InteractiveShell` and `ipykernel`.

    import ipykernel.kernelapp, nbconvert, traitlets, pidgy, types, pluggy, IPython, jinja2
    class pidgyShell(ipykernel.zmqshell.ZMQInteractiveShell):

The `pidgy` shell is wrapper around the existing `IPython` shell experience. It explicitly defines the tangle and weave conventions of literate programming to each interactive computing execution. Once the shell is configured, it can be reused as a `jupyter` kernel or `IPython` extension that supports the `pidgy` [Markdown]/[IPython] metalanguage and metasyntax.

        environment = traitlets.Any(nbconvert.exporters.TemplateExporter().environment)

## `pidgy` specification

        @pidgy.specification(firstresult=True)
        def tangle(str:str)->str:

The `tangle` step operates on an input string that will become compiled source code. In a literate program, the source is written primarily in the documentation language and tangling converts it to the programming language. In `pidgy`, the tangle steps target valid `IPython` which is a superset of [Python], and requires further processing.

        input_transformers_post = traitlets.List([pidgy.extras.demojize])

`pidgy` includes the ability the use emojis as valid python names through the existing `traitlets` configuration system.

        class pidgyManager(IPython.core.inputtransformer2.TransformerManager):
            def transform_cell(self, cell):
                shell = IPython.get_ipython()
                return super(type(self), self).transform_cell(
                    (shell and hasattr(shell, 'manager') and shell.manager.hook.tangle)(str=cell))

        input_transformer_manager = traitlets.Any(pidgyManager())

        ast_transformers = traitlets.List([pidgy.extras.ExtraSyntax(), pidgy.testing.Definitions()])

Another feature of `IPython` is the ability to intercept [Abstract Syntax Tree]s and change their representation or capture metadata. After these transformations are applied, `IPython` compile the tree into a valid `types.CodeType`.

        @pidgy.specification
        def post_execute(self):
            ...


        @pidgy.specification
        def post_run_cell(self, result):

The weave step happens after execution, the tangle step happens before. Weaving only occurs if the input is computationally verified. It allows different representations of the input to be displayed. `pidgy` will implement templated Markdown displays of the input and formally test the contents of the input.

        def _post_run_cell(self, result):
            self.manager.hook.post_run_cell(result=result)

        def _post_exec(self):
            self.manager.hook.post_execute()


        enable_html_pager = traitlets.Bool(True)
        definitions = traitlets.List()
        manager = traitlets.Instance('pluggy.PluginManager', args=('pidgy',))
        loaders = traitlets.Dict()

`pidgy` mixes the standard `IPython` configuration system and its own `pluggy` specification and implementation.

## Initializing the `pidgy` shell

        def init_pidgy(self):

Initialize `pidgy` specific behaviors.

            self.manager.add_hookspecs(pidgyShell)
            for object in (
                pidgy.tangle, pidgy.weave.Weave(shell=self), pidgy.testing, pidgy.extras
            ):

The tangle and weave implementations are discussed in other parts of this document. Here we register each of them as `pluggy` hook implementations.

                self.manager.register(object)
            self.events.register("post_run_cell", types.MethodType(pidgyShell._post_run_cell, self))
            self.events.register("post_execute", types.MethodType(pidgyShell._post_exec, self))


            if pidgy.pidgyLoader not in self.loaders:

`pidgy` enters a loader context allowing [Markdown] and notebook files to be used permissively as input.

                self.loaders[pidgy.pidgyLoader] = pidgy.pidgyLoader().__enter__()

It also adds a few extra features to the shell.

            self.user_ns["shell"] = self
            self.user_ns.update({k: v for k, v in vars(IPython.display).items()
                if pidgy.util.istype(v, IPython.core.display.DisplayObject)
            })

and allows json syntax as valid python input.

            pidgy.extras.init_json()

        def __init__(self, *args, **kwargs):

Override the initialization of the conventional IPython kernel to include the pidgy opinions.

            super().__init__(*args, **kwargs)
            self.init_pidgy()

## `pidgy` extension.

        def load_ipython_extension(shell):

The pidgy kernel makes it easy to access the pidgy shell, but it can also be used an IPython extension.

            shell.add_traits(manager=pidgyShell.manager, loaders=pidgyShell.loaders, definitions=pidgyShell.definitions)
            shell._post_run_cell = types.MethodType(pidgyShell._post_run_cell, shell)
            shell._post_exec = types.MethodType(pidgyShell._post_exec, shell)
            pidgyShell.init_pidgy(shell)
            shell.input_transformer_manager = pidgyShell.input_transformer_manager.default_value

<!--  -->

        def unload_ipython_extension(self):
            self.events.unregister("post_run_cell", self._post_run_cell)
            self.events.unregister("post_run_cell", pidgy.weave.post_run_cell)
            loader = self.loaders.pop(pidgy.pidgyLoader)
            if loader is not None:
                loader.__exit__(None, None, None)


    load_ipython_extension = pidgyShell.load_ipython_extension
    unload_ipython_extension = pidgyShell.unload_ipython_extension

[shell]: https://en.wikipedia.org/wiki/Shell_(computing)
[kernel]: https://en.wikipedia.org/wiki/Kernel_(operating_system)
[kernel languages]: https://github.com/jupyter/jupyter/wiki/Jupyter-kernels
