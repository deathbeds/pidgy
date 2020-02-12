from .. import pidgyLoader
with pidgyLoader():
    from .import cli
cli.application()