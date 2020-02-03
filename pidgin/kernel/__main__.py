import pidgin
with pidgin.translate.PidginLoader():
    from . import shell
print(shell.PidginKernelApp.kernel.default_value, shell.PidginKernelApp)
shell.PidginKernelApp.launch_instance()