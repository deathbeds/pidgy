# import sphinx.writers.html5
# sphinx.writers.html5.HTML5Translator.visit_pending_xref = lambda *x:...
# sphinx.writers.html5.HTML5Translator.depart_pending_xref = lambda *x:...
title = html_title = "pidgy literate computing"
author = "Tony Fast"
html_theme = "classic"
master_doc = "index"
source_suffix = ".rst .md .ipynb .py".split()
extensions = "recommonmark nbsphinx sphinx.ext.autodoc sphinx.ext.coverage sphinx.ext.napoleon autoapi.extension sphinx.ext.mathjax sphinx_copybutton     sphinx.ext.viewcode".split()

# Exclude build directory and Jupyter backup files:
exclude_patterns = ["_build", "*checkpoint*"]
autoapi_type = "python"
autoapi_dirs = ["pidgy"]

nbsphinx_prolog = """.. raw:: html
    
    <style>.prompt {
        display: none;
    }</style>


"""


def setup(app):
    if "READTHEDOCS" in __import__("os").environ:
        __import__("os").system("python -m pidgy to python pidgy/*.md --write")
