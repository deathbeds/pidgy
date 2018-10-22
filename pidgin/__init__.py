from ._version import *

with __import__('importnb').Notebook():
    from .markdown import MarkdownImporter
    from . import shell
    from . import kernel
    from . import macros
    
_ipython_display_ = shell._ipython_display_

import IPython

def load_ipython_extension(ip=None):
    ip = ip or IPython.get_ipython()
    MarkdownImporter().__enter__()
    # Jinja2Importer().__enter__()
    # Jinja2MarkdownImporter().__enter__()
    for module in (shell, kernel, macros):
        module.load_ipython_extension(ip)
    return __import__(__name__)
load = load_ipython_extension
def unload_ipython_extension(ip):
    MarkdownImporter().__exit__()
    # Jinja2Importer().__enter__()
    # Jinja2MarkdownImporter().__enter__()
    for module in (shell, kernel, macros):
        module.unload_ipython_extension(ip)
        
unload = unload_ipython_extension