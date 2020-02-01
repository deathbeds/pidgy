import pidgin
with pidgin.imports.PidginLoader():
    from . import shell
print(shell.PidginKernelApp.kernel.default_value, shell.PidginKernelApp)
shell.PidginKernelApp.launch_instance()