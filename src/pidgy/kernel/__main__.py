if __name__ == "__main__":
    import ipykernel.kernelapp

    from . import Kernel

    ipykernel.kernelapp.IPKernelApp.launch_instance(kernel_class=Kernel)
