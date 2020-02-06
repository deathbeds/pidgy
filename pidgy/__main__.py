from . import reuse
with reuse.pidgyLoader():
    from .import cli
cli.app()