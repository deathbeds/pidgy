from . import translate
with translate.pidgyLoader():
    from .import cli
cli.app()