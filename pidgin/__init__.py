
# coding: utf-8

# In[ ]:


def load_ipython_extension(ip):
    get_ipython().run_line_magic('reload_ext', 'importnb')
    from pidgin.config import alias
    if __name__ == '__main__':
        get_ipython().run_line_magic('reload_ext', 'config')
    else:
        get_ipython().run_line_magic('reload_ext', 'pidgin.config')


# In[ ]:


if __name__ == '__main__':
    get_ipython().system('jupyter nbconvert --to python __init__.ipynb')
    load_ipython_extension(__import__('IPython').get_ipython())

