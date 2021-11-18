from dataclasses import dataclass
from typing import Any


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


@dataclass
class Output:
    parent: Any
    display_cls: Any = None
    input: str = ""
    display_handle: Any = None
    cell_id: str = None
    vars: set = field(set)

    def set_input(self, input):
        from jinja2.meta import find_undeclared_variables

        self.input = input
        self.vars.clear()
        vars = find_undeclared_variables(self.parent.environment.parse(input))
        self.vars.update(vars)
        primary_loader = self.parent.environment.loader.loaders[0]
        primary_loader.mapping.update({self.cell_id: input})

    def _ipython_display_(self):
        from IPython.core.display import DisplayHandle

        if self.input.startswith(("http://", "https://")):
            lines = self.input.splitlines()
            if all(
                line.startswith(("http://", "https://"))
                for line in lines
                if line.strip()
            ):
                from mimetypes import guess_type

                from IPython.display import IFrame, Image, display

                displays = []
                for line in lines:
                    if line.strip():
                        type, _ = guess_type(line)
                        if type and type.startswith(("image/",)):
                            displays.append(Image(url=line))
                        else:
                            displays.append(
                                IFrame(
                                    line,
                                    height=self.parent.iframe_height,
                                    width="100%",
                                )
                            )
                return display(*displays)

        if self.display_handle is None:
            self.display_handle = DisplayHandle()
        if self.parent.reactive:
            self.display_handle.display(self.display_cls(""))
            if self.parent.asynch:
                from asyncio import ensure_future

                ensure_future(self.aupdate())
            else:
                self.update()
        else:
            self.display()

    @property
    def template(self):
        if self.cell_id:
            return self.parent.environment.get_template(self.cell_id)
        return self.parent.environment.from_string(self.input)

    def update(self):
        self.display_handle.update(
            self.display_cls(self.template.render(**self.parent.get_ns()))
        )

    def display(self):
        self.display_handle.display(
            self.display_cls(self.template.render(**self.parent.get_ns()))
        )

    async def aupdate(self):
        self.display_handle.update(
            self.display_cls(await self.template.render_async(**self.parent.get_ns()))
        )
