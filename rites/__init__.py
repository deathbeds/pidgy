
# coding: utf-8

# In[ ]:


if __name__ == '__main__':
    get_ipython().run_line_magic('load_ext', 'loader')
else:
    get_ipython().run_line_magic('load_ext', 'rites.loader')
from rites.config import alias
    
[alias.__setitem__(str, f"rites.{str}") for str in ('markdown', 'template', 'conventions', 'test')]

if __name__ == '__main__':
    get_ipython().run_line_magic('reload_ext', 'config')
    get_ipython().system('jupyter nbconvert --to python __init__.ipynb')
    load_ipython_extension()
else:
    get_ipython().run_line_magic('load_ext', 'rites.config')

