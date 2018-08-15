
# coding: utf-8

# In[1]:


with __import__('importnb').Notebook():
    from .markdown import MarkdownImporter
    # from .template import Jinja2Importer, Jinja2MarkdownImporter

def load_ipython_extension(ip):
    MarkdownImporter().__enter__()
    # Jinja2Importer().__enter__()
    # Jinja2MarkdownImporter().__enter__()
    from .extensions import load_ipython_extension
    load_ipython_extension(ip)