with __import__('importnb').Notebook():  
    from .. import tangle
    from . import transform_cell
with tangle.Pidgin():
    from .. import shell
    from . import emojis, yaml, json, transform_ast
    from . import  testing, markdown, template, colors
    