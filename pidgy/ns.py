"""enrich the base IPython namespace with other things we already have
these changes improve the author's throughput in interactive computing.
when a pidgy document becomes a script we need to explicitly add the imports"""
from . import get_ipython


def pre_execute():
    import sys

    ns = get_ipython().user_ns
    ns.update({k: v for k, v in sys.modules.items() if "." not in k and k not in ns})
    ns.update({k: v for k, v in ns.get("__annotations__", {}).items() if k not in ns})


def load_ipython_extension(shell):
    shell.events.register(pre_execute.__name__, pre_execute)


def unload_ipython_extension(shell):
    shell.events.unregister(pre_execute.__name__, pre_execute)
