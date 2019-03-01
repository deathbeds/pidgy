with __import__('importnb').Notebook():  
    from .. import tangle

with tangle.Pidgin(): 
    from . import do_inspect, publishing, loaders
    from .loaders import *

