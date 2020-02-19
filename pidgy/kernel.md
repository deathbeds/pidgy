    import jupyter_client, IPython, ipykernel.ipkernel, ipykernel.kernelapp, pidgy, traitlets, pidgy, traitlets, ipykernel.kernelspec, ipykernel.zmqshell, pathlib, traitlets

The shell is the application either jupyterlab or jupyter notebook, the kernel determines the programming language.  Below we design a just jupyter kernel that can be installed using 

```bash
pidgy kernel install
```

    _sep = __import__('itertools').cycle("|/-|\ ".strip())

    class pidgyInteractiveShell(ipykernel.zmqshell.ZMQInteractiveShell):
Configure a native `pidgy` `IPython.InteractiveShell`

        loaders = traitlets.List(allow_none=True)
        weave = traitlets.Any(allow_none=True)
        tangle = ipykernel.zmqshell.ZMQInteractiveShell.input_transformer_manager
        testing = traitlets.Any(allow_none=True)
        enable_html_pager = traitlets.Bool(True)
`pidgyInteractiveShell.enable_html_pager` is necessary to see rich displays in the inspector.

        def __init__(self,*args, **kwargs):
            super().__init__(*args, **kwargs)
            with pidgy.pidgyLoader():
                from .extension import load_ipython_extension
            load_ipython_extension(self)


    class pidgyKernel(ipykernel.ipkernel.IPythonKernel):
        shell_class = traitlets.Type(pidgyInteractiveShell)
        _last_parent = traitlets.Dict()

        def init_metadata(self, parent):
            self._last_parent = parent
            return super().init_metadata(parent)

        def do_inspect(self, code, cursor_pos, detail_level=0):
`pidgyKernel.do_inspect` will default to wysiwyg configuration thats displays a preview
of the source input rendered as markdown.

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


                code = self._make_time()+F"""<br/><code>·L{
                    len(lead.splitlines()) + int(not(col))
                },C{col + 1}</code><br/>\n\n""" + code[:cursor_pos]+'·'+('' if col else '<br/>\n')+code[cursor_pos:]

                object['data'] = {'text/markdown': code}
We include the line number and cursor position to enrich the connection between the inspector and the source code displayed on another part of the screen.

            return object

        def _make_time(self, t=None):
            import datetime, emoji

            days="twelve one two three four five six seven eight nine ten eleven"

            days = days.split()*2

            t = datetime.datetime.now() if t is None else t

            hour, minute = t.hour%12, t.minute
            _minute = str(t.minute)
            if len(_minute) == 1: _minute = '0'+_minute
            return "<code>"+ 'AP'[t.hour//12]+' '+''.join(
                emoji.EMOJI_UNICODE[F":{days[x]}_o’clock:"] + (
                    '' if x != 5 and (x+1)%3 else ' '
                ) for x in range(hour%12)
            ) + _minute + "</code>\n"
