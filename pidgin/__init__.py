
# coding: utf-8

# In[1]:


with __import__('importnb').Notebook():
    from .markdown import MarkdownImporter
    from .template import Jinja2Importer, Jinja2MarkdownImporter
        
def load_ipython_extension(ip):
    MarkdownImporter(display=True).__enter__()
    Jinja2Importer().__enter__()
    Jinja2MarkdownImporter(display=True).__enter__()
