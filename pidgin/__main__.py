with __import__('pidgin').imports.PidginLoader():
    try: from . import cli
    except: import cli
    
cli.app()