"""Registering `pidgy` extensions"""

import IPython, ipykernel.ipkernel, ipykernel.kernelapp, pidgy, traitlets, ipykernel.kernelspec, ipykernel.zmqshell, pathlib, pluggy, importnb

implementation = pluggy.HookimplMarker("pidgy")
specification = pluggy.HookspecMarker("pidgy")
plugin_manager = pluggy.PluginManager("pidgy")
