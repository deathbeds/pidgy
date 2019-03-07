with __import__('importnb').Notebook():  
    from .. import tangle

with tangle.Pidgin(): 
    from . import loaders, do_inspect, do_execute, do_complete, publishing
    from .loaders import *

