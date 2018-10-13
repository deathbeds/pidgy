from version import *

with __import__('importnb').Notebook():
    from .markdown import MarkdownImporter
    from . import magics
    from . import shell
    from . import kernel
    from . import stringdisplays

def load_ipython_extension(ip):
    MarkdownImporter().__enter__()
    # Jinja2Importer().__enter__()
    # Jinja2MarkdownImporter().__enter__()
    for module in (magics, shell, kernel, stringdisplays):
        module.load_ipython_extension(ip)