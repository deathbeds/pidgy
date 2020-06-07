# The `pidgy` literate computing shell

A powerful feature of the `jupyter` ecosystem is a generalized implementation of the [shell] & [kernel] model for interactive computing interfaces like the terminal and notebooks. That is to say that different programming languages can use the same interface, `jupyter` supports [over 100 languages now][kernel languages]. The general ability to support different languages is possible because of configurable interfaces like the `IPython.InteractiveShell` and `ipykernel`.

    import ipykernel.kernelapp, ipykernel.zmqshell, nbconvert, traitlets, pidgy, types, pluggy, IPython, jinja2
    class pidgyShell(ipykernel.zmqshell.ZMQInteractiveShell):

The `pidgy` shell is wrapper around the existing `IPython` shell experience. It explicitly defines [tangle] and [weave] conventions of literate programming for each execution. Once the shell is configured, it can be used as a `jupyter` kernel or `IPython` extension that supports the `pidgy` [Markdown]/[IPython] metalanguage and metasyntax.

## `pidgy` specification

        input_transformers_post = traitlets.List([pidgy.tangle.demojize])

`pidgy` includes the ability the use emojis as valid python names through the existing `traitlets` configuration system.

        @traitlets.default('input_transformer_manager')
        def _default_input_transform_manager(self):
            return pidgy.tangle.pidgyManager()

        ast_transformers = traitlets.List([pidgy.tangle.ExtraSyntax()])

Another feature of `IPython` is the ability to intercept [Abstract Syntax Tree]s and change their representation or capture metadata. After these transformations are applied, `IPython` compile the tree into a valid `types.CodeType`.

        @pidgy.specification
        def post_execute(self):
            ...


        @pidgy.specification
        def post_run_cell(self, result, shell):

The weave step happens after execution, the tangle step happens before. Weaving only occurs if the input is computationally verified. It allows different representations of the input to be displayed. `pidgy` will implement templated Markdown displays of the input and formally test the contents of the input.

        environment = traitlets.Any(nbconvert.exporters.TemplateExporter().environment)

`pidgy` includes a `jinja2` templating environment that allows live compute to be woven into a narrative.

        def _post_run_cell(self, result):
            self.manager.hook.post_run_cell(result=result, shell=self)

        def _post_exec(self):
            self.manager.hook.post_execute()


        enable_html_pager = traitlets.Bool(True)
        definitions = traitlets.List()
        manager = traitlets.Instance('pluggy.PluginManager', args=('pidgy',))
        loaders = traitlets.Dict()
        weave = traitlets.Any()
        testing = traitlets.Any()

        @traitlets.default('weave')
        def _default_weave(self): return pidgy.weave.Weave(parent=self)
        @traitlets.default('testing')
        def _default_testing(self): return pidgy.testing.Testing(parent=self)

`pidgy` mixes the standard `IPython` `traitlets` configuration system and its own `pluggy` `specification` and `implementation`.

## Initializing the `pidgy` shell

        def init_pidgy(self):

Initialize `pidgy` specific behaviors.

            if self.weave is None:
                self.weave = pidgyShell._default_weave(self)

            try:
                self.manager.add_hookspecs(pidgyShell)
                for object in (
                    self.weave, self.testing
                ):

The tangle and weave implementations are discussed in other parts of this document. Here we register each of them as `pluggy` hook implementations.

                    self.manager.register(object)
            except AssertionError:...
            self.ast_transformers.append(self.testing.visitor)
            self.events.register("post_run_cell", types.MethodType(pidgyShell._post_run_cell, self))
            self.events.register("post_execute", types.MethodType(pidgyShell._post_exec, self))


            if pidgy.pidgyLoader not in self.loaders:

`pidgy` enters a loader context allowing [Markdown] and notebook files to be used permissively as input.

                self.loaders[pidgy.pidgyLoader] = pidgy.pidgyLoader().__enter__()

It also adds a few extra features to the shell.

            self.user_ns.update(pidgy.util.pidgy_builtins())

and allows json syntax as valid python input.

            pidgy.tangle.init_json()
            pidgy.magic.load_ipython_extension(self)

        def __init__(self, *args, **kwargs):

Override the initialization of the conventional IPython kernel to include the pidgy opinions.

            super(type(self), self).__init__(*args, **kwargs)
            self.init_pidgy()

[shell]: https://en.wikipedia.org/wiki/Shell_(computing)
[kernel]: https://en.wikipedia.org/wiki/Kernel_(operating_system)
[kernel languages]: https://github.com/jupyter/jupyter/wiki/Jupyter-kernels
