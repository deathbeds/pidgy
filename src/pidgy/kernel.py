"""a modified pidgy kernel.

the command line application installs the kernel"""

from contextlib import suppress

from ipykernel.ipkernel import IPythonKernel


class Kernel(IPythonKernel):
    # help_links = List([]).tag(config=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shell.magics_manager.magics["line"]["reload_ext"]("pidgy")


if __name__ == "__main__":
    import ipykernel.kernelapp

    ipykernel.kernelapp.IPKernelApp.launch_instance(kernel_class=Kernel)
