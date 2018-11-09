from ._version import *
from .loader import PidginImporter

with __import__('importnb').Notebook():
    from . import shell
    from . import kernel
    from . import formatter

import IPython

def load_ipython_extension(ip=None):
    ip = ip or IPython.get_ipython()
    for module in (shell, formatter): module.load_ipython_extension(ip)
    try:
        kernel.load_ipython_extension(ip)
    except AttributeError: "There is no kernel to replace"

load = load_ipython_extension

def unload_ipython_extension(ip):
    for module in (shell, formatter):
        module.unload_ipython_extension(ip)
    try:
        kernel.unload_ipython_extension(ip)
    except: "There is no kernel to replace"

unload = unload_ipython_extension
