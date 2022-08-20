from .pidgy import Extension


def load_ipython_extension(shell):
    from .weave import IPyWidgetsHtml
    shell.displays_manager.template_cls = IPyWidgetsHtml

    from ipywidgets import Widget
    import ipywidgets
    for k, v in vars(ipywidgets).items():
        if isinstance(v, type) and issubclass(v, Widget):
            if k[0].isupper():
                shell.user_ns.setdefault(k, v)


def unload_ipython_extension(_):
    pass
