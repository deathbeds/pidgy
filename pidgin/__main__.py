from __init__ import imports
with imports.PidginLoader():
    try: from . import cli
    except: import cli
    
cli.pidgin()