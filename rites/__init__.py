
# coding: utf-8

# In[14]:


if __name__ == '__main__':
    get_ipython().run_line_magic('load_ext', 'loader')
else:
    get_ipython().run_line_magic('load_ext', 'rites.loader')
from rites.config import alias
    
[alias.__setitem__(str, f"rites.{str}") for str in ('markdown', 'template', 'conventions', 'test')]


# In[15]:


def load_ipython_extension(ip):
    if __name__ == '__main__':
        get_ipython().run_line_magic('reload_ext', 'config')
    else:
        get_ipython().run_line_magic('load_ext', 'rites.config')


# In[ ]:


if __name__ == '__main__':
    get_ipython().system('jupyter nbconvert --to python __init__.ipynb')
    load_ipython_extension(__import__('IPython').get_ipython())

