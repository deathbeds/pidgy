from . import loader

with loader.pidgyLoader():
    from . import readme

readme.application()
