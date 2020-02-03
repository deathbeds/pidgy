import pidgy
with pidgy.translate.pidgyLoader():
    from . import shell
print(shell.pidgyKernelApp.kernel.default_value, shell.pidgyKernelApp)
shell.pidgyKernelApp.launch_instance()