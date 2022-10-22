from collections import defaultdict
from dataclasses import dataclass, field
from io import StringIO
from re import compile
from typing import ChainMap

from jinja2 import Environment, Template
from jinja2.meta import find_undeclared_variables
from markdown_it import MarkdownIt
from traitlets import Bool, Dict, Instance, Type

from .pidgy import Extension

CELL_MAGIC = compile("^\s*%{2}\S")
NO_SHOW = compile(r"^\s*\r?\n")

from IPython import get_ipython


class Finalizer:
    def __new__(cls, object):
        return object


class IPythonFinalizer(Finalizer):
    @staticmethod
    def normalize(type, object, metadata) -> str:
        """normalize and object with (mime)type and return a string."""

        if type == "text/html" or "svg" in type:
            object = get_minified(object)

        if type.startswith("image"):
            md = metadata.get(type, {})
            width, height = md.get("width"), md.get("height")
            object = get_decoded(object)
            *_, data = type.partition("/")
            object = f"""<img src="data:image/{data};base64,{object}"/>"""

        return object

    def __new__(cls, object):
        """convert an object into a markdown/html representation"""
        from IPython import get_ipython

        shell = get_ipython()
        datum = shell.display_formatter.format(object)
        data, metadata = datum if isinstance(datum, tuple) else (datum, {})
        key = next(filter(data.__contains__, get_active_types(shell)), str(object))
        if key == "text/plain":
            return str(object)
        return cls.normalize(key, data[key], metadata)


class IPythonEnvironment(Environment):
    def init_filters(self):
        try:
            from nbconvert.exporters.templateexporter import default_filters

            self.filters.update(default_filters)
        except ModuleNotFoundError:
            pass

    def __init__(self, *args, **kwargs):
        from jinja2 import ChoiceLoader, DictLoader, Environment, FileSystemLoader

        kwargs.setdefault("loader", ChoiceLoader([DictLoader({}), FileSystemLoader(".")]))
        kwargs.setdefault("finalize", IPythonFinalizer)
        kwargs.setdefault("undefined", Undefined)
        kwargs.setdefault("enable_async", False)  # enable this later
        super().__init__(*args, **kwargs)
        self.init_filters()


from jinja2 import Undefined


class IPythonTemplate(Template):
    def ns(self, *args, **kwargs):
        import builtins

        ns = get_ipython()
        if ns:
            return ChainMap(kwargs, ns.user_ns, vars(builtins))
        return {}

    def render(self, *args, **kwargs):
        return super().render(self.ns(*args, **kwargs))

    async def render_async(self, *args, **kwargs):
        return await super().render_async(self.ns(*args, **kwargs))


class Undefined(Undefined):
    def _fail_with_undefined_error(self, *args, **kwargs):
        # log that the template failed
        return f"`{self._undefined_name} is undefined`"


@dataclass
class TemplateDisplay:
    widget = False
    from IPython.display import Markdown

    template: object = None
    display_cls: type = Markdown
    display_handle: object = None
    iframe_attrs: dict = field(default_factory=dict(width="100%", height=600, loading="lazy").copy)
    is_list_urls: bool = None
    vars: set = field(default_factory=set)
    # this is not used by the base class but may be used by other base classes that render html
    markdown_renderer: object = field(default_factory=MarkdownIt)

    del Markdown

    def _ipython_display_(self):
        self.display()

    def _is_list_urls(self, x):
        for line in filter(bool, map(str.strip, StringIO(x))):
            if "://" in line:
                continue
            return False
        return True

    def render(self):
        render = self.template.render()
        if self.is_list_urls is None:
            self.is_list_urls = self._is_list_urls(render)

        # if self.is_list_urls:
        #     render = self.embed(render)

        return render

    def update(self, change=None):
        # it should be possible to do smarter updates
        if self.display_handle:
            if self.is_widget():
                self.display_handle.value = self.render()
            else:
                self.display_handle.update(self.display_cls(self.render()))

    def embed(self, urls):
        """we have a feature for showing iframes of urls.

        we can add richer features later like domain rules and file extension dispatchers
        maybe the could have been done with markdown it?"""
        lines = []

        # compose the default iframe attributes
        args = " ".join(f'{k}="{v}"' for k, v in self.iframe_attrs.items())

        # iterate through all the lines of the source and generate iframes
        # from them.
        for line in filter(bool, map(str.strip, StringIO(urls))):
            lines.append(f'<iframe src="{line}" {args}/>')
        return "\n".join(lines)


@dataclass
class IPythonMarkdown(TemplateDisplay):
    def display(self):
        from IPython.display import display

        if self.display_handle is None:
            from IPython.display import DisplayHandle

            self.display_handle = DisplayHandle()

        object = self.display_cls(self.render())
        self.display_handle.display(object)

    def update(self, change=None):
        if self.display_handle:
            self.display_handle.update(self.display_cls(self.render()))


class MarkdownItMixin:
    def render(self):
        return self.markdown_renderer.render(super().render())


@dataclass
class IPythonHtml(MarkdownItMixin, IPythonMarkdown):
    from IPython.display import HTML

    display_cls: type = HTML
    del HTML


@dataclass
class IPyWidgetsHtml(MarkdownItMixin, TemplateDisplay):
    widget = True
    from ipywidgets import HTML

    display_cls: object = HTML
    del HTML

    def display(self):
        from IPython.display import display

        if self.display_handle is None:
            self.display_handle = self.display_cls(self.render())
        display(self.display_handle)

    def update(self, change=None):
        if self.display_handle:
            self.display_handle.value = self.render()


class DisplaysManager(Extension):
    displays = Dict()
    prior = Dict()
    template_cls = Type(IPythonMarkdown, TemplateDisplay)
    markdown_renderer = Instance(MarkdownIt, args=())
    reactive = Bool(True)
    widgets = Dict()

    def weave_cell(self, body):
        template = self.shell.environment.from_string(body, None, IPythonTemplate)
        vars = find_undeclared_variables(self.shell.environment.parse(body))
        # print(888, vars)
        return self.template_cls(
            template=template, vars=vars, markdown_renderer=self.markdown_renderer
        )

    def get_value(self, key, raw=True):
        """get a value in a namespace that is potentially a widgets."""
        value = self.shell.user_ns.get(key)

        if raw:
            return value

        if is_widget(value):
            return value.value

        return value

    def get_id(self):
        return self.shell.kernel.get_parent().get("metadata", {}).get("cellId")

    def get_vars(self):
        data = defaultdict(list)
        for d in self.displays.values():
            for k in d.vars:
                data[k].append(d)

        return data

    def link_widgets(self):
        # collect all the widgets into a dict
        # link widgets to a display
        displays_by_key = self.get_vars()
        olds = list()
        # print(self.displays, displays_by_key)
        for key, displays in displays_by_key.items():
            value = self.get_value(key)
    
            if is_widget(value):
                if self.widgets.setdefault(key, value) is not value:
                    olds.append(self.widgets[key])
                    self.widgets[key] = value

                for display in displays:
                    value.observe(display.update, "value")                

        for old in olds:
            old.close()

    def post_run_cell(self, result):
        from IPython.display import display

        id = self.get_id()
        if result.error_in_exec or result.error_before_exec:
            pass  # don't do anything when there are errors
        elif NO_SHOW.match(result.info.raw_cell):
            pass
        elif CELL_MAGIC.match(result.info.raw_cell):
            pass
        else:
            disp = self.displays[id] = self.weave_cell(result.info.raw_cell)
            display(self.displays[id])
            return

        self.displays.pop(id, None)

    def pre_execute(self):
        metadata = self.shell.kernel.get_parent().get("metadata", {})
        for id in metadata.get("deletedCells", []):
            if id in self.displays:
                del self.displays[id]

        vars = set()
        for id, disp in self.displays.items():
            if disp.vars:
                vars.update(disp.vars)
        self.prior.update(zip(vars, map(self.get_value, vars)))

    def post_execute(self):
        changed = set()

        for k, v in self.prior.items():
            y = self.get_value(k)
            if y is not v:
                changed.update({k})

        for id, disp in self.displays.items():
            changed.intersection(disp.vars) and disp.update()

        if self.reactive:
            self.link_widgets()


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
    return x


def get_decoded(object):
    if isinstance(object, bytes):
        from base64 import b64encode

        object = b64encode(object).decode("utf-8")
    return object


def get_environment(reuse=True, _cache={}, **kwargs):
    # use this function to avoid repeat environment instantiation
    shell = get_ipython()
    if shell:
        try:
            return shell.environment
        except AttributeError:
            pass
    if reuse:
        if _cache:
            return _cache[True]
        _cache[True] = IPythonEnvironment(**kwargs)
        return _cache[True]
    return IPythonEnvironment(**kwargs)


def is_widget(object):
    """is an object a widget"""
    from sys import modules

    if "ipywidgets" in modules:
        from ipywidgets import Widget

        return isinstance(object, Widget)
    return False


def load_ipython_extension(shell):
    shell.add_traits(environment=Instance(IPythonEnvironment, default_value=get_environment()))
    shell.add_traits(displays_manager=Instance(Extension, allow_none=True))
    shell.displays_manager = DisplaysManager(shell=shell, markdown_renderer=shell.tangle.parser)
    shell.displays_manager.load_ipython_extension()


def unload_ipython_extension(shell):
    DisplaysManager(shell=shell).unload_ipython_extension()
