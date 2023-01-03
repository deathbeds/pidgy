def register_ipython_extensions():
    pass


class Extension(HasTraits):
    from . import IS_IPY

    IS_IPY = True

    alias = CUnicode(allow_none=True)
    shell = Instance("IPython.InteractiveShell")
    enabled = Bool(True)

    def __init_subclass__(cls, alias=None, **kwargs):
        if alias:
            cls.alias = CUnicode(default=alias)
        super().__init_subclass__(**kwargs)

    def load_ipython_extension(self):
        # if self.register:
        #     # register a trait with a specific name on the current shell
        #     if not self.shell.has_trait(self.alias):
        #         self.shell.add_traits(**{self.alias: Instance(type(self))})

        #     # set the attribute on the shell
        #     setattr(self.shell, self.alias, self)

        # register any methods corresponding the shell events callbacks names
        for event in self.shell.events.callbacks:
            property = getattr(self, event, None)
            if property is not None:
                self.shell.events.register(event, property)

        vars = set(dir(self))

        for magic in set(MAGICS).intersection(vars):
            self.shell.register_magic_function(getattr(self, magic), magic, self.alias)

        if isinstance(self, NodeTransformer):
            self.shell.ast_transformers.append(self)

        for transform in TRANSFORMS.intersection(vars):
            getattr(self.shell.input_transformer_manager, transform).insert(
                0, getattr(self, transform)
            )

        return self

    def unload_ipython_extension(self):
        for event, callers in self.shell.events.callbacks.items():
            this = type(self)
            if this:
                for caller in callers:
                    if issubclass(type(caller.__self__), Extension):
                        self.shell.events.unregister(event, caller)

        vars = set(dir(self))

        if isinstance(self, NodeTransformer):
            self.shell.ast_transformers = [x for x in self.shell.ast_transformers if x is not self]

        for transform in TRANSFORMS.intersection(vars):
            f = getattr(type(self), transform)
            ts = getattr(self.shell.input_transformer_manager, transform)

            transforms = [t for t in ts if getattr(type(t), transform, None) is not f]
            setattr(self.shell.input_transformer_manager, transform, transforms)

        return self
