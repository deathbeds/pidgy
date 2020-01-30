import importnb
with importnb.Notebook():
    try: from . import imports
    except: import imports

with imports.PidginLoader():
    try: 
        from . import appendix
        from .implementation import load_ipython_extension, unload_ipython_extension
    except: 
        import appendix
        from implementation import load_ipython_extension, unload_ipython_extension
    
    