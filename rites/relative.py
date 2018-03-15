
# coding: utf-8

# # by *convention* __import__s should be the same

# In[1]:


...; o = __name__ == '__main__'; ...;


# Relative imports in the notebook are not allowed.

# In[2]:


if o:
    try: from . import relative
    except ImportError: assert True


# This means _when a notebook is used as source_, relative imports have an unexpected behavior.
# 
# This notebook will `load_ipython_extension`s that allow relative imports by replacing them with the `blank` convention below ⬇️

# In[3]:


blank = """try: 
    from . import object
except: 
    import object"""


# ---
# #### parent __import__s
# 
# > It is not possible to __import__ a notebook above the current directory so there no reason to implement higher-level __import__s.

# In[4]:


if o:
    try: from .. import object
    except ValueError as Exception: 
        assert Exception.args == ('attempted relative import beyond top-level package',)


# ---
# 
# ## The `Relative` `ast.NodeTransformer`

# In[5]:


from ast import parse, NodeTransformer, copy_location
class Relative(NodeTransformer):
    """Replace __import__ when {node.level is 1} with the `try` statement in {blank}."""
    blank = parse(blank).body[0]
    def visit_ImportFrom(Relative, node):
        if node.module : return node
        if node.level is 1:
            Relative.blank.body[0].names =             Relative.blank.handlers[0].body[0].names = node.names
            return copy_location(Relative.blank, node)
        return node


# ## The Extensions
# 
#     %unload rites.relative

# In[6]:


def unload_ipython_extension(ip=get_ipython()): return [
    object for object in ip.ast_transformers if not isinstance(object, Relative)]


#     %reload rites.relative

# In[7]:


def load_ipython_extension(ip=get_ipython()): ip.ast_transformers = unload_ipython_extension(ip) +[Relative()]


# ## Developer

# ### Testing
# 
# Test the `rites.relative` extension on itself; remove any python files for the test.

# In[8]:


if o:
    get_ipython().run_line_magic('reload_ext', 'rites')
    load_ipython_extension()
    get_ipython().run_line_magic('rm', 'relative.py')


# In[9]:


from . import relative


# In[ ]:


__test__ = dict(
    imports=""">>> assert relative is relative.relative""",
    file=""">>> assert relative.__file__.endswith('.ipynb')""",
    type=""">>> assert isinstance(relative, __import__('types').ModuleType)""")


# ### Tear Down
# 
# > Export the `relative.ipynb` as a python script because it does not rely on anything from `rites`.

# In[ ]:


if o:
    __import__('doctest').testmod(verbose=2)
    get_ipython().system('jupyter nbconvert --to python relative.ipynb')

