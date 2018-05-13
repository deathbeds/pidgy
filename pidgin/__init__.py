
# coding: utf-8

# In[1]:


def load_ipython_extension(ip):
    get_ipython().run_line_magic('reload_ext', 'importnb')
    from pidgin.config import alias
    if __name__ == '__main__':
        get_ipython().run_line_magic('reload_ext', 'config')
    else:
        get_ipython().run_line_magic('reload_ext', 'pidgin.config')


# In[6]:


from IPython.core.inputsplitter import IPythonInputSplitter


# In[7]:


def unload_ipython_extension(ip):
    ip.input_transformer_manager = IPythonInputSplitter()


# In[2]:


if __name__ == '__main__':
    get_ipython().system('jupyter nbconvert --to python __init__.ipynb')
load_ipython_extension(__import__('IPython').get_ipython())

