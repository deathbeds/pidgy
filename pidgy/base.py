"""Registering `pidgy` extensions"""

import IPython, ast, dataclasses, functools, importnb


@dataclasses.dataclass
class Extension:
    """`Extension` is base class that simplifies loading and unloading IPython extensions. Each component of `pidgy` is an IPython extension are this work compacts some repetative practices."""

    _repl_events = "pre_execute pre_run_cell post_execute post_run_cell".split()
    shell: IPython.InteractiveShell = dataclasses.field(
        default_factory=IPython.get_ipython
    )

    def register(self, shell=None, *, method=""):
        if shell:
            self.shell = shell
        register, unregister = not bool(method), bool(method)
        shell = self.shell
        for event in self._repl_events:
            callable = getattr(self, event, None)
            callable and getattr(shell.events, f"{method}register")(event, callable)
        if isinstance(self, ast.NodeTransformer):
            register and shell.ast_transformers.append(self)
            unregister and shell.ast_transformers.pop(
                shell.ast_transformers.index(self)
            )

            if isinstance(self, IPython.core.inputtransformer2.TransformerManager):
                if register:
                    shell.input_transformer_manager = self
                if unregister:
                    shell.input_transformer_managers = (
                        IPython.core.inputtransformer2.TransformerManager()
                    )

        return self

    unregister = functools.partialmethod(register, method="un")
