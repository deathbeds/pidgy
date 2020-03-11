# `pidgy` shell and kernel

> A kernel provides programming language support in Jupyter. IPython is the default kernel. Additional kernels include R, Julia, and many more.
>
> > - [`jupyter` kernel definition](https://jupyter.readthedocs.io/en/latest/glossary.html#term-kernel)

`pidgy` is a wrapper kernel around the
existing `ipykernel and IPython.InteractiveShell` configurables.
`IPython` adds extra syntax to python that simulate literate programming
macros.

![](https://jupyter.readthedocs.io/en/latest/_images/other_kernels.png)

<!--

    import jupyter_client, IPython, ipykernel.ipkernel, ipykernel.kernelapp, pidgy, traitlets, pidgy, traitlets, ipykernel.kernelspec, ipykernel.zmqshell, pathlib, traitlets

-->

The shell is the application either jupyterlab or jupyter notebook, the kernel
determines the programming language. Below we design a just jupyter kernel that
can be installed using

- What is the advantage of installing the kernel and how to do it.

```bash
pidgy kernel install
```

    class pidgyInteractiveShell(ipykernel.zmqshell.ZMQInteractiveShell):

Configure a native `pidgy` `IPython.InteractiveShell`

        loaders = traitlets.Dict(allow_none=True)
        weave = traitlets.Any(allow_none=True)
        tangle = traitlets.Any(allow_none=True)
        extras = traitlets.Any(allow_none=True)
        testing = traitlets.Any(allow_none=True)
        measure = traitlets.Any(allow_none=True)
        enable_html_pager = traitlets.Bool(True)

`pidgyInteractiveShell.enable_html_pager` is necessary to see rich displays in
the inspector.

        def __init__(self,*args, **kwargs):
            super().__init__(*args, **kwargs)
            with pidgy.pidgyLoader():
                from .extension import load_ipython_extension
            self.user_ns['shell'] = self
            load_ipython_extension(self)

    class pidgyKernel(ipykernel.ipkernel.IPythonKernel):
        shell_class = traitlets.Type(pidgyInteractiveShell)
        _last_parent = traitlets.Dict()

        def init_metadata(self, parent):
            self._last_parent = parent
            return super().init_metadata(parent)

The `pidgy` kernel command line features.

    def install()->None:

`install` the pidgy kernel.

import click
manager = **import**('jupyter_client').kernelspec.KernelSpecManager()
path = str((pathlib.Path(**file**).parent / 'kernelspec').absolute())
try:
dest = manager.install_kernel_spec(path, 'pidgy')
except:
click.echo(F"System install was unsuccessful. Attempting to install the pidgy kernel to the user.")
dest = manager.install_kernel_spec(path, 'pidgy', True)
click.echo(F"The pidgy kernel was install in {dest}")

<!---->

    def uninstall()->None:

`uninstall` the kernel.

        import jupyter_client, click
        jupyter_client.kernelspec.KernelSpecManager().remove_kernel_spec('pidgy')
        click.echo(F"The pidgy kernel was removed.")

<!---->

    def start(f:str="")->None:

Launch a `pidgy` kernel applications.

        ipykernel.kernelapp.IPKernelApp.launch_instance(
            kernel_class=pidgyKernel)
    ...
