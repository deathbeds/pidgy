"""Reactive IPython/IPywidgets templates

these displays combine IPython displays with jinja2 environments.
we export multiple displays to use in different contexts.
for example, voila prefers HTML ipywidgets based displays to gain interactivity.
"""
# in this module we try to shield the library imports to make
# dependencies optional. we always have markdown it and ipython.
# ipywidgets may be optional

from dataclasses import dataclass, field
from io import StringIO
from re import compile
from IPython.display import DisplayHandle, display, HTML, Markdown

from markdown_it import MarkdownIt
from asyncio import ensure_future
from . import get_ipython

URL = compile("^(http[s]|file)://")


@dataclass
class TemplateDisplay:
    """the TemplateDisplays base class that provides the api for displaying and updating templates."""

    body: str = None
    template: object = None
    display_cls: type = Markdown
    display_handle: object = None
    iframe_attrs: dict = field(default_factory=dict(width="100%", height=600, loading="lazy").copy)
    is_list_urls: bool = None
    vars: set = field(default_factory=set)
    # this is not used by the base class but may be used by other base classes that render html
    tokens: object = None
    markdown_renderer: object = None
    use_async: bool = True

    def _ipython_display_(self):
        """display the template contents"""
        if self.display_handle is None:
            self.display_handle = DisplayHandle()

        if self.use_async and get_ipython().weave.reactive:
            self.display_handle.display(self.display_object(self.body))
            ensure_future(self.aupdate())
        else:
            try:
                import nest_asyncio

                nest_asyncio.apply()
            except ModuleNotFoundError:
                raise ImportError("nest_asyncio is needed to use synchronous rendering.")
            self.display_handle.display(self.display_object(self.render()))

    def _is_list_urls(self, x):
        for line in filter(bool, map(str.strip, StringIO(x))):
            if URL.match(line):
                continue

            return False
        return True

    async def arender(self):
        """async template rendering"""
        output = StringIO()

        try:
            async for part in self.template.generate_async():
                output.write(part)
        except BaseException as e:
            import traceback

            msg = "".join(traceback.format_exception(type(e), e, e.__traceback__))
            return f"""`````````pytb\n{msg}\n`````````"""
        return output.getvalue()

    def render(self):
        """sync template rendering"""
        return self.template.render()

    def display_object(self, object, **kwargs):
        return self.display_cls(object, **kwargs)

    async def aupdate(self):
        # it should be possible to do smarter updates
        if self.display_handle:
            self.display_handle.update(self.display_object(await self.arender()))

    def observe(self, _):
        ensure_future(self.aupdate())

    def is_widget(self):
        return is_widget(self.display_handle)

    def update(self):
        # it should be possible to do smarter updates
        if self.display_handle:
            self.display_handle.update(self.display_object(self.render()))

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
    pass


@dataclass
class MarkdownItMixin:
    markdown_renderer: object = field(default_factory=MarkdownIt)

    async def arender(self):
        return self.markdown_renderer.render(await super().arender())


@dataclass
class IPythonHtml(MarkdownItMixin, IPythonMarkdown):
    display_cls: type = HTML


@dataclass
class IPyWidgetsHtml(MarkdownItMixin, TemplateDisplay):
    display_cls: "ipywidgets.Widget" = None

    def __post_init__(self):
        if self.display_cls is None:
            from ipywidgets import HTML

            self.display_cls = HTML

    async def aupdate(self):
        if self.display_handle:
            self.display_handle.value = await self.arender()

    def _ipython_display_(self):
        if self.display_handle is None:
            self.display_handle = self.display_object("")

        if self.use_async:
            display(self.display_handle)
            ensure_future(self.aupdate())
        else:
            display(self.display_object(self.render()))


def is_widget(object):
    from sys import modules

    if "ipywidgets" in modules:
        from ipywidgets import Widget

        return isinstance(object, Widget)
    return False
