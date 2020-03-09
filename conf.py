# import sphinx.writers.html5
# sphinx.writers.html5.HTML5Translator.visit_pending_xref = lambda *x:...
# sphinx.writers.html5.HTML5Translator.depart_pending_xref = lambda *x:...
html_theme = 'classic'
master_doc = 'index'
source_suffix = '.rst .md .ipynb'.split()
extensions = 'recommonmark nbsphinx'.split() 

# Exclude build directory and Jupyter backup files:
exclude_patterns = ['_build', '**.ipynb_checkpoints']
