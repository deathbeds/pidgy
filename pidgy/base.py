"""Registering `pidgy` extensions"""

import IPython, ipykernel.ipkernel, ipykernel.kernelapp, pidgy, traitlets, ipykernel.kernelspec, ipykernel.zmqshell, pathlib, pluggy

implementation = pluggy.HookimplMarker("pidgy")
specification = pluggy.HookspecMarker("pidgy")


class pidgyShell(ipykernel.zmqshell.ZMQInteractiveShell):

    enable_html_pager = traitlets.Bool(True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin_manager = pluggy.PluginManager("pidgy")
        self.plugin_manager.add_hookspecs(type(self))
        for plugin in (pidgy.tangle, pidgy.weave, pidgy.testing):
            self.plugin_manager.register(plugin)

        self.input_transformer_manager.line_transforms.append(pidgy.extras.demojize)
        self.ast_transformers.append(pidgy.extras.ExtraSyntax())
        pidgy.pidgyLoader().__enter__()
        self.events.register(
            "post_run_cell",
            lambda result: self.plugin_manager.hook.weave(result=result),
        )
        self.user_ns["shell"] = self

    @specification(firstresult=True)
    def tangle(self, text: str):
        ...

    def transform_cell(self, str):
        return super().transform_cell(self.plugin_manager.hook.tangle(text=str))

    @specification
    def weave(self, result):
        ...
