with __import__('importnb').Notebook(lazy=True):
    try: from . import imports
    except: import imports

with imports.PidginLoader(lazy=True):
    try: 
        from . import appendix
        from .extension import load_ipython_extension, unload_ipython_extension
    except: 
        import appendix
        from extension import load_ipython_extension, unload_ipython_extension

