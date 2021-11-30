def field(default=None, description=None, **metadata):
    from dataclasses import field

    param = {callable(default) and "default_factory" or "default": default}
    if description:
        metadata["description"] = description
    return field(metadata=metadata or None, **param)


def get_ipython():
    import IPython

    shell = IPython.get_ipython()
    if shell is None:
        shell = IPython.InteractiveShell()
        IPython.get_ipython = shell.get_ipython
    return shell


def get_active_types(shell=None):
    """get the active types in the current IPython shell.
    we ignore latex, but i forget why."""
    shell = shell or get_ipython()
    if shell:
        object = list(shell.display_formatter.active_types)
        object.insert(object.index("text/html"), object.pop(object.index("text/latex")))
        return reversed(object)
    return []


def get_minified(x):
    from htmlmin import minify

    return minify(x, False, True, True, True, True, True, True)


def get_decoded(object):
    if isinstance(object, bytes):
        from base64 import b64encode

        object = b64encode(object).decode("utf-8")
    return object


def is_widget(object):
    """is an object a widget"""
    from sys import modules

    if "ipywidgets" in modules:
        from ipywidgets import Widget

        return isinstance(object, Widget)
    return False


def was_displayed(object):
    # the best we can know is if the widget was ever displayed
    return object._trait_values.get("_display_callbacks") is not None


def is_list_of_url(str):
    return all(
        line.startswith(("http://", "https://"))
        for line in str.splitlines()
        if line.strip()
    )


def get_escaped_string(object, quote='"'):
    from re import subn

    return subn(r"%s{1,1}" % quote, "\\" + quote, object)[0]
