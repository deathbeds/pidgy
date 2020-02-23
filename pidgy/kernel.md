# Configuring the `pidgy` shell and kernel architecture.

`IPython` provides two kernel architectures.

At this point, we can imagine `pidgy` implementations in other languages.

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
        testing = traitlets.Any(allow_none=True)
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

        def do_inspect(self, code, cursor_pos, detail_level=0):

`pidgyKernel.do_inspect` will default to wysiwyg configuration thats displays a
preview of the source input rendered as markdown.

yyy!!!

            object = {'found': False}
            if code[:cursor_pos][-3:] == '!!!':
                object = {'found': True, 'data': {'text/markdown': self.shell.weave.format_markdown(code[:cursor_pos-3]+code[cursor_pos:])}}
            else:
                try:
                    object = super().do_inspect(code, cursor_pos, detail_level=0)
                except: ...

            if not object['found']:

Simulate finding an object and return a preview of the markdown.

                object['found'] = True
                line, offset = IPython.utils.tokenutil.line_at_cursor(code, cursor_pos)
                lead = code[:cursor_pos]
                col = cursor_pos - offset


                code = F"""<code>·L{
                    len(lead.splitlines()) + int(not(col))
                },C{col + 1}</code><br/>\n\n""" + code[:cursor_pos]+'·'+('' if col else '<br/>\n')+code[cursor_pos:]

                object['data'] = {'text/markdown': code}

We include the line number and cursor position to enrich the connection between
the inspector and the source code displayed on another part of the screen.

            return object
