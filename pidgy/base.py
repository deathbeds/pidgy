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
    plugin_manager = pluggy.PluginManager("pidgy")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pidgy.pidgyLoader().__enter__()
        for plugin in (pidgy.tangle, pidgy.weave, pidgy.testing):
            self.plugin_manager.register(plugin)
        self.events.register(
            "post_run_cell", lambda x: self.plugin_manager.hook.weave(result=x)
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


pidgyShell.plugin_manager.add_hookspecs(pidgyShell)
