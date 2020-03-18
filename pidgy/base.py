"""Registering `pidgy` extensions"""

import IPython, ipykernel.ipkernel, ipykernel.kernelapp, pidgy, traitlets, ipykernel.kernelspec, ipykernel.zmqshell, pathlib, pluggy, importnb

implementation = pluggy.HookimplMarker("pidgy")
specification = pluggy.HookspecMarker("pidgy")

with importnb.Notebook():
    try:
        from . import extras
    except:
        import extras


class pidgyShell(ipykernel.zmqshell.ZMQInteractiveShell):

    enable_html_pager = traitlets.Bool(True)
    ast_transformers = traitlets.List([extras.ExtraSyntax()]).tag(config=True)
    input_transformers_post = traitlets.List([extras.demojize])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin_manager = pluggy.PluginManager("pidgy")
        self.plugin_manager.add_hookspecs(type(self))
        for plugin in (pidgy.tangle, pidgy.weave, pidgy.testing):
            self.plugin_manager.register(plugin)

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
