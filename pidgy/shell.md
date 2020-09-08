# the `pidgy` shell

    import ipykernel.kernelapp, ipykernel.zmqshell, traitlets, pidgy, types, IPython, jinja2
    

`pidgy` relies on the `jupyter` [shell] & [kernel] to provide an enhanced authoring experience for computational documentations.  the [kernel] has the ability to work with the cpu, memory, and other devices; the [shell] is the application we use to affect changes to the kernel.

the `jupyter` ecosystem has grown include more [over 100 languages now][kernel languages]. Most recently, it has brought new life to compiled languages like [C++](https://github.com/jupyter-xeus/xeus-cling) and [Fortran](https://github.com/lfortran/lfortran/).

A powerful feature of the `jupyter` ecosystem is a generalized implementation of the [shell] & [kernel] model for interactive ctomputing interfaces like the terminal and notebooks. That is to say that different programming languages can use the same interface, `jupyter` supports [over 100 languages now][kernel languages]. The general ability to support different languages is possible because of configurable interfaces like the `IPython.InteractiveShell` and `ipykernel`.

    
    class pidgyShell(ipykernel.zmqshell.ZMQInteractiveShell):

`pidgy` introduces markdown as an application language for literate computing. it encodes the tangle and weave aspects of literate programming directly into the interactive cell execution. with each execution, the input is _tangled_ into valid `IPython` source code then the input is processed as [markdown] output with `jinja2` templates.

## tangle markdown to code

        @traitlets.default('input_transformer_manager')
        def _default_tangle(self): 
`pidgy` tangles [markdown] to source code on block elements permitting line-for-line transforms to `IPython`. The [tangle](tangle.ipynb) section contains more detail on this heurisitic.
        
            return pidgy.tangle.pidgyManager()

we can already use existing `IPython` features to transform the abstract syntax tree and apply text processing. `pidgy` includes the abilities to:

* use emojis in code

        input_transformers_post = traitlets.List([pidgy.tangle.demojize])

* use return statements at the top code level, outside of functions, to display objects.

        ast_transformers = traitlets.List([pidgy.tangle.ExtraSyntax()])


## weave input to output

        weave = traitlets.Any()
        @traitlets.default('weave')
        def _default_weave(self): 
`pidgy` weaves the input into a rich display provided by `jupyter` display system, it adds the ability to implicitly transclude variables from live compute into a narrative. in traditional literate computing, code and narrative had to be mixed explicitly.
        
            return pidgy.weave.Weave(parent=self)

## formal interactive testing

        testing = traitlets.Any()
        @traitlets.default('testing')
        def _default_testing(self): 
`pidgy` promotes value by including formal testing it literate programs.

            testing = pidgy.testing.Testing(parent=self)
            self.ast_transformers.append(testing.visitor)
            return testing


## import alternative document formats

        loaders = traitlets.Dict()

        def init_loaders(self):
`pidgy` augments the python import system to include `pidgy` notebooks and markdown documents along with normal notebooks.

            for x in (pidgy.pidgyLoader, __import__("importnb").Notebook):
                if x not in self.loaders:
                    self.loaders[x] = x().__enter__()

## extra shell initialization options

        def init_pidgy(self):
            if self.weave is None:
                self.weave = pidgyShell._default_weave(self)
            if self.testing is None:
                self.testing = pidgyShell._default_testing(self)


            for x in (self.weave, self.testing):
                try: x.register()
                except AssertionError:...

            pidgyShell.init_loaders(self)
            pidgy.magic.load_ipython_extension(self)
            __import__('importlib').reload(__import__('doctest'))

        enable_html_pager = traitlets.Bool(True)
        
        def __init__(self, *args, **kwargs):
Override the initialization of the conventional IPython kernel to include the pidgy opinions.

            super(type(self), self).__init__(*args, **kwargs)
            self.init_pidgy()

    
[shell]: https://en.wikipedia.org/wiki/Shell_(computing)
[kernel]: https://en.wikipedia.org/wiki/Kernel_(operating_system)
[kernel languages]: https://github.com/jupyter/jupyter/wiki/Jupyter-kernels