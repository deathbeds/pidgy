"""Reactive IPython/IPywidgets templates
"""
# in this module we try to shield the library imports to make
# dependencies optional. we always have markdown it and ipython.
# ipywidgets may be optional

from dataclasses import dataclass, field
from io import StringIO
from re import compile

from markdown_it import MarkdownIt

URL = compile("^(http[s]|file)://")


@dataclass
class TemplateDisplay:
    """the TemplateDisplays base class that provides the api for displaying and updating templates."""

    widget = False
    from IPython.display import Markdown

    body: str = None
    template: object = None
    display_cls: type = Markdown
    display_handle: object = None
    iframe_attrs: dict = field(default_factory=dict(width="100%", height=600, loading="lazy").copy)
    is_list_urls: bool = None
    vars: set = field(default_factory=set)
    # this is not used by the base class but may be used by other base classes that render html
    markdown_renderer: object = field(default_factory=MarkdownIt)
    tokens: object = None

    del Markdown

    def _ipython_display_(self):
        self.display()

    def _is_list_urls(self, x):
        for line in filter(bool, map(str.strip, StringIO(x))):
            if URL.match(line):
                continue

            return False
        return True

    def render(self):
        render = self.template.render()
        if self.is_list_urls is None:
            self.is_list_urls = self._is_list_urls(render)

        if self.is_list_urls:
            return self.embed(render)

        return render

    def display_object(self, object, **kwargs):
        # metadata = self.get_markdown_metadata()
        # if metadata:
        #     kwargs.setdefault("metadata", {"@graph": metadata})
        return self.display_cls(object, **kwargs)

    def update(self, change=None):
        # it should be possible to do smarter updates
        if self.display_handle:
            render = self.render()

            if is_widget(self.display_handle):
                self.display_handle.value = render
            else:
                self.display_handle.update(self.display_object(render))

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
        from IPython.display import HTML, display

        if self.display_handle is None:
            from IPython.display import DisplayHandle

            self.display_handle = DisplayHandle()

        object = self.render()
        if self.is_list_urls:
            self.display_cls = HTML

        self.display_handle.display(self.display_object(object))


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
    display_cls: object = None

    def __post_init__(self):
        if self.display_cls is None:
            from ipywidgets import HTML

            self.display_cls = HTML

    def display(self):
        from IPython.display import DisplayHandle, display

        if self.display_handle is None:
            self.display_handle = DisplayHandle()
        md = {}  # self.get_markdown_metadata()
        self.display_handle.display(
            self.display_cls(self.render()),
            metadata=md,
        )


def is_widget(object):
    """is an object a widget"""
    from sys import modules

    if "ipywidgets" in modules:
        from ipywidgets import Widget

        return isinstance(object, Widget)
    return False
