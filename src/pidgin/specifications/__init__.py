with __import__('importnb').Notebook():  
    from .. import tangle
    from . import transform_cell, emojis_, yaml_, json, transform_ast, template

with tangle.Pidgin(lazy=True):
    from . import testing, markdown