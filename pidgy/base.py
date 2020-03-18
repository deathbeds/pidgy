import pluggy

implementation = pluggy.HookimplMarker("pidgy")
specification = pluggy.HookspecMarker("pidgy")
plugin_manager = pluggy.PluginManager("pidgy")
