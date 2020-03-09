# import sphinx.writers.html5
# sphinx.writers.html5.HTML5Translator.visit_pending_xref = lambda *x:...
# sphinx.writers.html5.HTML5Translator.depart_pending_xref = lambda *x:...
title = html_title = "pidgy literate computing"
author = "Tony Fast"
html_theme = "classic"
master_doc = "index"
source_suffix = ".rst .md .ipynb .py".split()
extensions = "recommonmark nbsphinx sphinx.ext.autodoc sphinx.ext.coverage sphinx.ext.napoleon autoapi.extension".split()

# Exclude build directory and Jupyter backup files:
exclude_patterns = ["_build", "*checkpoint*"]
autoapi_type = "python"
autoapi_dirs = ["pidgy"]
