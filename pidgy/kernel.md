# `pidgy` shell and kernel

![](https://jupyter.readthedocs.io/en/latest/_images/other_kernels.png)

Interactive programming in `pidgy` documents is accessed using the polyglot
[Jupyter] kernel architecture. In fact, the provenance the [Jupyter]
name is a combination the native kernel architectures for
[ju~~lia~~][julia], [pyt~~hon~~][python], and [r]. [Jupyter]'s
generalization of the kernel/shell interface allows
over 100 languages to be used in `notebook and jupyterlab`.
It is possible to define prescribe wrapper kernels around existing
methods; this is the appraoach that `pidgy` takes

> A kernel provides programming language support in Jupyter. IPython is the default kernel. Additional kernels include R, Julia, and many more.
>
> > - [`jupyter` kernel definition](https://jupyter.readthedocs.io/en/latest/glossary.html#term-kernel)

`pidgy` is not not a native kernel. It is a wrapper kernel around the
existing `ipykernel and IPython.InteractiveShell` configurables.
`IPython` adds extra syntax to python that simulate literate programming
macros.

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

## Configure the `pidgy` shell.

    class pidgyInteractiveShell(ipykernel.zmqshell.ZMQInteractiveShell):

Configure a native `pidgy` `IPython.InteractiveShell`

        loaders = traitlets.Dict(allow_none=True)
        weave = traitlets.Any(allow_none=True)
        tangle = ipykernel.zmqshell.ZMQInteractiveShell.input_transformer_manager
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
            load_ipython_extension(self)

## Configure the `pidgy` kernel.

    class pidgyKernel(ipykernel.ipkernel.IPythonKernel):
        shell_class = traitlets.Type(pidgyInteractiveShell)
        _last_parent = traitlets.Dict()

        def init_metadata(self, parent):
            self._last_parent = parent
            return super().init_metadata(parent)
