from ._version import *
from .loader import PidginImporter

with __import__('importnb').Notebook():
    from . import shell
    from . import kernel
    from . import display

import IPython

def load_ipython_extension(ip=None):
    ip = ip or IPython.get_ipython()
    for module in (shell, kernel, display): module.load_ipython_extension(ip)

load = load_ipython_extension

def unload_ipython_extension(ip):
    for module in (shell, display, kernel):
        module.unload_ipython_extension(ip)

unload = unload_ipython_extension
