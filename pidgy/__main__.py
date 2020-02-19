from . import reuse
with reuse.pidgyLoader():
    from . import readme
print(11)
readme.application()