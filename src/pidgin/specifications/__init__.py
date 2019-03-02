with __import__('importnb').Notebook():  
    from .. import tangle
    from . import transform_cell, emojis_, yaml_, json, transform_ast

with tangle.Pidgin():
    from .. import shell
    from . import  testing, markdown, template
    