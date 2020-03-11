from . import loader, autocli

with loader.pidgyLoader():
    from . import readme, kernel
import click

application = autocli.autoclick(
    readme.run,
    readme.test,
    autocli.autoclick(
        kernel.install, kernel.uninstall, kernel.start, group=click.Group("kernel")
    ),
    context_settings=dict(allow_extra_args=True),
)

application()
