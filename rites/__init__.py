
# coding: utf-8

# In[ ]:


try:
    from .loader import load_ipython_extension, unload_ipython_extension 
except:
    from loader import load_ipython_extension, unload_ipython_extension 
finally:
    load_ipython_extension()
    
from rites.config import alias
    
[alias.__setitem__(str, f"rites.{str}") for str in ('markdown', 'template', 'conventions', 'test')]

if __name__ == '__main__':
    get_ipython().run_line_magic('reload_ext', 'config')
    get_ipython().system('jupyter nbconvert --to python __init__.ipynb')
    load_ipython_extension()
else:
    get_ipython().run_line_magic('load_ext', 'rites.config')

