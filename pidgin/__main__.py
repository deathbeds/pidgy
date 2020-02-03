from . import imports
with imports.PidginLoader():
    from .import cli
cli.app()