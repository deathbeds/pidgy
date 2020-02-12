from . import reuse
with reuse.pidgyLoader():
    from .app import cli
cli.application()