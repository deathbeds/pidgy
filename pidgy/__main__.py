from . import loader

with loader.pidgyLoader():
    from .readme import application

application()
