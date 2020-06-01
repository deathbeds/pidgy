import pluggy, traitlets

implementation = pluggy.HookimplMarker("pidgy")
specification = pluggy.HookspecMarker("pidgy")
plugin_manager = pluggy.PluginManager("pidgy")


class Trait(traitlets.HasTraits):
    parent = traitlets.Any()
