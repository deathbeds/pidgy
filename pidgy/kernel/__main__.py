with __import__('pidgy').reuse.pidgyLoader():
    from . import shell 
__import__('ipykernel').kernelapp.IPKernelApp.launch_instance(kernel_class=shell.pidgyKernel)