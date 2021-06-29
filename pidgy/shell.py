import IPython


class Shell(IPython.InteractiveShell):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from . import load_ipython_extension

        load_ipython_extension(self)
