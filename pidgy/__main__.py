from . import reuse
with reuse.pidgyLoader():
    from .readme import application
    
application()