"""a modified pidgy kernel.

the command line application installs the kernel"""

from contextlib import suppress

from ipykernel.ipkernel import IPythonKernel


class Kernel(IPythonKernel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from . import load_ipython_extension

        load_ipython_extension(self.shell)


if __name__ == "__main__":
    import ipykernel.kernelapp

    ipykernel.kernelapp.IPKernelApp.launch_instance(kernel_class=Kernel)
