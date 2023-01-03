"""a modified pidgy kernel.

the command line application installs the kernel"""

from contextlib import suppress
from sys import argv

from ipykernel.ipkernel import IPythonKernel


class Kernel(IPythonKernel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.shell.magics_manager.magics["line"]["reload_ext"]("pidgy")
