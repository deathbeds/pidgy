"""the pidgy kernel, a runner for the pidgy kernel"""
import contextlib

import ipykernel.ipkernel


class Kernel(ipykernel.ipkernel.IPythonKernel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from . import load_ipython_extension

        load_ipython_extension(self.shell)

    def init_metadata(self, object):
        self.shell.last_parent = object
        return ipykernel.ipkernel.IPythonKernel.init_metadata(self, object)

    def do_inspect(self, code, cursor_pos, detail_level=0):
        from . import weave
        return super().do_inspect(code, cursor_pos, detail_level)
        if code[:cursor_pos].rstrip()[-3:] == "!!!":
            if code[:cursor_pos].rstrip()[-6:] == "!!!" * 2:
                self.shell.run_cell(code[:cursor_pos], silent=True)
                
            return self.markdown_result(self.shell.displays_manager.get_display(code[:cursor_pos]).data)
        result = super().do_inspect(code, cursor_pos, detail_level)
        if not result["found"]:
            return self.markdown_result(code)
        return result

    def markdown_result(self, code):
        return dict(found=True, status="ok", metadata={}, data={"text/markdown": code})

    def do_complete(self, code, cursor_pos):
        return super().do_complete(code, cursor_pos)

    @classmethod
    def patch(cls):
        import types

        import ipykernel.ipkernel

        from . import get_ipython

        shell = get_ipython()
        for x in "init_metadata do_complete do_inspect".split():
            if getattr(shell.kernel, x).__func__ == getattr(
                ipykernel.ipkernel.IPythonKernel, x
            ):
                setattr(
                    shell.kernel, x, types.MethodType(getattr(Kernel, x), shell.kernel)
                )

    @classmethod
    def unpatch(cls):
        import types

        import ipykernel.ipkernel

        from . import get_ipython

        shell = get_ipython()
        for x in "init_metadata do_complete do_inspect".split():
            if getattr(shell.kernel, x).__func__ != getattr(
                ipykernel.ipkernel.IPythonKernel, x
            ):
                setattr(
                    shell.kernel,
                    x,
                    types.MethodType(
                        getattr(ipykernel.ipkernel.IPythonKernel, x), shell.kernel
                    ),
                )


def pre_run_cell(x):
    from . import get_ipython

    shell = get_ipython()
    if shell.last_parent:
        md = shell.last_parent["metadata"]
        shell.id = md.get("cellId")
        shell.cell_ids.add(shell.id)
        for k in md.get("deletedCells", ()):
            with contextlib.suppress(KeyError):
                shell.cell_ids.remove(k)
        if shell.id:
            shell.cell_ids.add(shell.id)


def load_ipython_extension(shell):
    import traitlets

    shell.add_traits(
        last_parent=traitlets.Any(), cell_ids=traitlets.Set(), id=traitlets.Any()
    )
    shell.events.register(pre_run_cell.__name__, pre_run_cell)
    Kernel.patch()


def unload_ipython_extension(shell):
    with contextlib.suppress(ValueError):

        shell.events.unregister(pre_run_cell.__name__, pre_run_cell)
    Kernel.unpatch()


if __name__ == "__main__":
    import ipykernel.kernelapp

    from . import shell

    ipykernel.kernelapp.IPKernelApp.launch_instance(kernel_class=Kernel)
