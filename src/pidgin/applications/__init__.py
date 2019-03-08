with __import__('importnb').Notebook():  
    from .. import tangle

with tangle.Pidgin(): 
    from . import do_inspect, do_execute, do_complete, publishing, loaders
    from .loaders import *
