# `pidgy` kernel

> A kernel provides programming language support in Jupyter. IPython is the default kernel. Additional kernels include R, Julia, and many more.
>
> > - [`jupyter` kernel definition](https://jupyter.readthedocs.io/en/latest/glossary.html#term-kernel)

`pidgy` is a wrapper kernel around the
existing `ipykernel and IPython.InteractiveShell`.

![](https://jupyter.readthedocs.io/en/latest/_images/other_kernels.png)

    import IPython, ipykernel.ipkernel, ipykernel.kernelapp, pidgy, traitlets, ipykernel.kernelspec, ipykernel.zmqshell, pathlib

    class pidgyKernel(ipykernel.ipkernel.IPythonKernel):

The `pidgy` kernel specifies to `jupyter` how it can be used as a native kernel from
the launcher or notebook. It specifies which shell class to use.

        shell_class = traitlets.Type('pidgy.shell.pidgyShell')
        loaders = traitlets.Dict()
        _last_parent = traitlets.Dict()
        current_cell_id = traitlets.Unicode()
        current_cell_ids = traitlets.Set()

        def init_metadata(self, object):

The is some important data captured in the initial we'll expose for later.

            self.shell._last_parent = object
            return super().init_metadata(object)

        def do_inspect(self, code, cursor_pos, detail_level=0):

The kernel is where the inspection can be customized. `pidgy` adds the ability to use
the inspector as Markdown rendering tool.

            if code[:cursor_pos].rstrip()[-3:] == '!!!':
                if code[:cursor_pos].rstrip()[-6:] == '!!!'*2:
                    self.shell.run_cell(code[:cursor_pos], silent=True)
                return self.markdown_result(self.shell.weave.render(code[:cursor_pos]))
            result = super().do_inspect(code, cursor_pos, detail_level)
            if not result['found']: return self.markdown_result(code)
            return result

        def markdown_result(self, code):
            return dict(found=True, status='ok', metadata={}, data={'text/markdown': code})

        def do_complete(self, code, cursor_pos):

The kernel even allows the completion system to be modified.

            return super().do_complete(code, cursor_pos)

## `pidgy` kernel installation

    def install():

`install` the pidgy kernel.

        import jupyter_client, click
        manager = jupyter_client.kernelspec.KernelSpecManager()
        path = str((pathlib.Path(__file__).parent / 'kernelspec').absolute())
        try:
            dest = manager.install_kernel_spec(path, 'pidgy')
        except:
            click.echo(F"System install was unsuccessful. Attempting to install the pidgy kernel to the user.")
        dest = manager.install_kernel_spec(path, 'pidgy', True)
        click.echo(F"The pidgy kernel was install in {dest}")

<!---->

    def uninstall():

`uninstall` the kernel.

        import jupyter_client, click
        jupyter_client.kernelspec.KernelSpecManager().remove_kernel_spec('pidgy')
        click.echo(F"The pidgy kernel was removed.")

<!---->

    def start(f:str=""):

Launch a `pidgy` kernel applications.

        ipykernel.kernelapp.IPKernelApp.launch_instance(connection_file=f, kernel_class=pidgyKernel)
    ...
