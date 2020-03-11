from . import loader, autocli

with loader.pidgyLoader():
    from . import readme, kernel, export
import click

application = autocli.autoclick(
    readme.run,
    readme.render,
    readme.test,
    export.convert,
    autocli.autoclick(
        kernel.install, kernel.uninstall, kernel.start, group=click.Group("kernel")
    ),
    context_settings=dict(allow_extra_args=True, ignore_unknown_options=True),
)

application()
