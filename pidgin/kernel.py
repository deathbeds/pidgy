with __import__('importnb').Notebook():
    from .kernel import PidginKernel
    
if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=PidginKernel)
