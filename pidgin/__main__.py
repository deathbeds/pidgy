from . import translate
with translate.PidginLoader():
    from .import cli
cli.app()