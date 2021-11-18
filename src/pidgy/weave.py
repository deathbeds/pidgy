from typing import Any

from .models import Weave, dataclass, field
from .utils import get_ipython, is_widget

__all__ = ("Weave",)


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

    def display_urls(self):
        lines = self.input.splitlines()
        from mimetypes import guess_type

        from IPython.display import IFrame, Image

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
        return displays

    def _ipython_display_(self):
        from IPython.core.display import DisplayHandle, display
        from .utils import is_list_of_url

        if is_list_of_url(self.input):
            return display(*self.display_urls())

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


@dataclass
class Weave(Weave):
    @staticmethod
    def get_environment(async_=False, ENVS={}):
        """retrieve singleton jinja2 environment."""
        from jinja2 import ChoiceLoader, DictLoader, Environment, FileSystemLoader

        # we maintain sync and async environments separately
        if async_ in ENVS:
            return ENVS[async_]

        ENVS[async_] = ENVIRONMENT = Environment(
            enable_async=async_,
            loader=ChoiceLoader([DictLoader({}), FileSystemLoader(".")]),
            cache_size=0,
            undefined=Weave.Undefined,
            finalize=Weave.Finalize(),
        )

        return ENVIRONMENT

    vars: set = field(set)
    prior: dict = field(dict)
    widgets: set = field(set)
    outputs: dict = field(dict)
    shell: Any = field(get_ipython, "the current interactive shell")
    environment: Any = field(get_environment, "a jinja templating environment")
    iframe_height: int = field(600, "the height of an iframe when urls are found")

    def use_asynch(self, input=True):
        self.asynch = input
        self.environment = self.get_environment(input)

    def __post_init__(self):
        self.use_asynch(self.asynch)

    from jinja2 import Undefined

    class Undefined(Undefined):
        def _fail_with_undefined_error(self, *args, **kwargs):
            # log that the template failed
            return f"`{self._undefined_name} is undefined`"

    class Finalize:
        """a callable trait that uses the current ipython display formatter to update jinja2 templates."""

        def normalize(self, type, object, metadata) -> str:
            """normalize and object with (mime)type and return a string."""
            from .utils import get_decoded, get_minified

            if type == "text/html" or "svg" in type:
                object = get_minified(object)

            if type.startswith("image"):
                width, height = (
                    metadata.get(type, {}).get("width"),
                    metadata.get(type, {}).get("height"),
                )
                object = get_decoded(object)
                object = f"""<img src="data:image/{type.partition('/')[2]};base64,{object}"/>"""
            return object

        def __call__(self, object):
            """convert an object into a markdown/html representation"""
            from .utils import get_active_types

            datum = get_ipython().display_formatter.format(object)
            data, metadata = datum if isinstance(datum, tuple) else (datum, {})
            try:
                key = next(filter(data.__contains__, get_active_types(get_ipython())))
            except StopIteration:
                return str(object)
            if key == "text/plain":
                return str(object)
            return self.normalize(key, data[key], metadata)

    def post_run_cell(self, result):
        if result.error_in_exec or result.error_before_exec:
            pass  # don't do anything when there are errors
        elif not self.no_show.match(result.info.raw_cell):
            from IPython.display import display

            metadata = self.shell.kernel.get_parent().get("metadata", {})
            id = metadata.get("cellId")
            output = self.outputs.setdefault(
                id, Output(parent=self, cell_id=id, display_cls=self.display_cls)
            )
            output.set_input(result.info.raw_cell)
            display(output)
            self.vars.update(output.vars)

    def pre_execute(self):
        from .utils import is_widget

        self.vars.clear()
        self.vars.update(*(x.vars for x in self.outputs.values()))

        metadata = self.shell.kernel.get_parent().get("metadata", {})
        for id in metadata.get("deletedCells", []):
            self.outputs.pop(id, None)

        self.widgets.clear()
        for k in self.vars:
            if k in self.shell.user_ns:
                x = self.prior[k] = self.shell.user_ns.get(k)
                if is_widget(x) and hasattr(x, "value"):
                    self.prior[k] = self.prior[k].value
                    self.widgets.add(x)
            self.prior.setdefault(k, None)

    def post_execute(self):
        if self.reactive:
            metadata = self.shell.kernel.get_parent().get("metadata", {})
            id, ns = metadata.get("cellId"), self.get_ns()
            updated, outputs_to_update = set(), []
            for k, v in self.prior.items():
                if v is ns.get(k):
                    continue
                elif k in self.widgets and v is getattr(ns.get(k), "value"):
                    continue
                updated.add(k)
            for output in self.outputs.values():
                if output.cell_id == id:
                    continue
                output.vars.intersection(updated) and outputs_to_update.append(output)
            if outputs_to_update:
                if self.asynch:
                    from asyncio import ensure_future, gather

                    ensure_future(gather(*(x.aupdate() for x in outputs_to_update)))
                else:
                    for x in outputs_to_update:
                        x.update()

    def get_ns(self):
        from collections import ChainMap
        from sys import modules

        public_ns = lambda k: k and k[0].isalpha() and "." not in k
        modules = {k: v for k, v in modules.items() if public_ns(k)}
        return dict(ChainMap(self.shell.user_ns, vars(__import__("builtins")), modules))

    def load(self):
        self.shell.events.register("pre_execute", self.pre_execute)
        self.shell.events.register("post_run_cell", self.post_run_cell)
        self.shell.events.register("post_execute", self.post_execute)

    def unload(self):
        self.shell.events.unregister("pre_execute", self.pre_execute)
        self.shell.events.unregister("post_run_cell", self.post_run_cell)
        self.shell.events.unregister("post_execute", self.post_execute)


def load_ipython_extension(shell):
    from IPython.display import Markdown
    from traitlets import Instance

    if not shell.has_trait("weave"):
        shell.add_traits(weave=Instance(Weave, ()))
    shell.weave = Weave(
        shell=shell,
        display_cls=Markdown,
        environment=Weave.get_environment(True),
        reactive=True,
    )
    shell.weave.load()


def unload_ipython_extension(shell):
    shell.has_trait("weave") and shell.weave.unload()
