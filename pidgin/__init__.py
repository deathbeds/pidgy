from ._version import *
with __import__('importnb').Notebook():
    from . import shell
    from . import tangle
    from . import kernel
    from . import display
    from .loader import PidginImporter


import IPython

def load_ipython_extension(ip=None):
    ip = ip or IPython.get_ipython()
    for module in (shell, kernel, display, tangle): module.load_ipython_extension(ip)

load = load_ipython_extension

def unload_ipython_extension(ip):
    for module in (shell, display, kernel, tangle):
        module.unload_ipython_extension(ip)

unload = unload_ipython_extension
