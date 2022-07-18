"""the extras extension adds features that improve interactive computing

1. exposes the `shell` variable for quick access to the interactive instance.
2. each execution the sys modules are populated in the namespace.
  
  this feature minimizes time between computing iterations by bringing more completion sooner.
  in an interactive computing session, the sys modules hold variable names not available to
  the author, but when available help continue flow between executions.
"""

from sys import modules
import IPython


def update_sys_modules():
    """update the shell's user namespace to include imported modules"""
    shell = IPython.get_ipython()
    shell.user_ns.update(
        (k, v)
        for k, v in modules.items()
        if k and k[0] != "_" and "." not in k and k not in shell.user_ns
    )


def load_ipython_extension(shell: IPython.InteractiveShell):
    shell.user_ns.setdefault("shell", shell)
    shell.events.register("pre_execute", update_sys_modules)


def unload_ipython_extension(shell: IPython.InteractiveShell):
    shell.events.unregister("pre_execute", update_sys_modules)
