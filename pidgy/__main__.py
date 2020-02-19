from . import reuse
with reuse.pidgyLoader():
    from . import readme
readme.application()