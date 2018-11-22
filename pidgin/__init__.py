from ._version import *
with __import__('importnb').Notebook():
    from . import post_run_cell
    from . import tangle
    from . import inspector
    from . import display
    from .loader import PidginImporter


import IPython

def load_ipython_extension(ip=None):
    ip = ip or IPython.get_ipython()
    for module in (post_run_cell, inspector, display, tangle): module.load_ipython_extension(ip)

load = load_ipython_extension

def unload_ipython_extension(ip):
    for module in (post_run_cell, inspector, display, tangle):
        module.unload_ipython_extension(ip)

unload = unload_ipython_extension
