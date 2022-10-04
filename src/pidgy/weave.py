from collections import defaultdict
from io import StringIO
from markdown_it import MarkdownIt
from dataclasses import dataclass, field
from typing import ChainMap
from jinja2 import Environment, Template
from traitlets import Dict, Instance, Type, Bool
from jinja2.meta import find_undeclared_variables
from pidgy import markdown
from pidgy.utils import get_ipython, is_widget
from .pidgy import Extension
from .models import CELL_MAGIC, _RE_BLANK_LINE as NO_SHOW


class Finalizer:
    def __new__(cls, object):
        return object


class IPythonFinalizer(Finalizer):
    @staticmethod
    def normalize(type, object, metadata) -> str:
        """normalize and object with (mime)type and return a string."""
        from .utils import get_decoded, get_minified

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
        from .utils import get_active_types
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

        kwargs.setdefault(
            "loader", ChoiceLoader([DictLoader({}), FileSystemLoader(".")])
        )
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
    vars: set = None
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

        object = self.display_cls(self.template.render())
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
    template_cls = Type(IPyWidgetsHtml, TemplateDisplay)
    markdown_renderer = Instance(MarkdownIt, args=())
    reactive = Bool(True)
    widgets = Dict()

    def weave_cell(self, body):
        template = self.shell.environment.from_string(body, None, IPythonTemplate)
        vars = find_undeclared_variables(self.shell.environment.parse(body))
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
            if d.widget:
                for k in d.vars:
                    data[k].append(d)

        return data

    def link_widgets(self):
        displays = self.get_vars()
        for k, disp in displays.items():
            v = self.get_value(k)
            if is_widget(v):
                if v is not self.widgets.get(k):
                    self.widgets[k] = v
                    for d in disp:
                        v.observe(d.update)

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
        if self.reactive:
            self.link_widgets()

        for k, v in self.prior.items():
            y = self.get_value(k)
            if y is not v:
                changed.update({k})

        for id, disp in self.displays.items():
            changed.intersection(disp.vars) and disp.update()


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


def load_ipython_extension(shell):
    shell.add_traits(
        environment=Instance(IPythonEnvironment, default_value=get_environment())
    )
    shell.add_traits(displays_manager=Instance(Extension, allow_none=True))
    shell.displays_manager = DisplaysManager(shell=shell)
    shell.displays_manager.load_ipython_extension()


def unload_ipython_extension(shell):
    DisplaysManager(shell=shell).unload_ipython_extension()
