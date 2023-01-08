from collections import defaultdict
from dataclasses import dataclass, field
from io import StringIO
from re import compile
from typing import ChainMap
from asyncio import ensure_future, gather

from jinja2 import Environment, Template
from jinja2.meta import find_undeclared_variables
from markdown_it import MarkdownIt
from traitlets import Bool, Dict, Instance, Type, HasTraits, observe, Enum

from .displays import IPythonMarkdown, TemplateDisplay, is_widget
from .environment import IPythonTemplate
from . import get_ipython

CELL_MAGIC = compile("^\s*%{2}\S")
NO_SHOW = compile(r"^\s*\r?\n")

URL = compile("^(http[s]|file)://")


class Weave(HasTraits):
    displays = Dict()
    shell = Instance("IPython.InteractiveShell", ())
    prior = Dict()  # prior value to compare against when reacting to updates
    template_type = Enum(["markdown", "html", "widget"]).tag(config=True)
    template_cls = Type(IPythonMarkdown, TemplateDisplay)
    markdown_renderer = Instance(MarkdownIt, args=())
    reactive = Bool(True).tag(config=True)
    use_async = Bool(True).tag(config=True)
    widgets = Dict()

    @observe("template_type")
    def _set_template_cls(self, value):
        from .displays import IPythonMarkdown, IPyWidgetsHtml, IPythonHtml

        self.template_cls = dict(markdown=IPythonMarkdown, widget=IPyWidgetsHtml, html=IPythonHtml)[
            self.template_type
        ]

    def get_template_vars(self, body):
        return find_undeclared_variables(self.shell.environment.parse(body))

    async def aweave_cell(self, body):
        template = self.shell.environment.from_string(
            body, None, IPythonTemplate, enable_async=True
        )
        return self.template_cls(
            body=body,
            template=template,
            vars=self.get_template_vars(body),
            markdown_renderer=self.markdown_renderer,
            use_async=self.use_async,
        )

    def filter_meta_tokens(self, body):
        if self.shell.pidgy.current_execution:
            for token in self.shell.pidgy.current_execution.tokens:
                if token.type in {"front_matter", "shebang"}:
                    continue
                break
            return "".join(body.splitlines(1)[token.map[0] :])
        return body

    def weave_cell(self, body):
        body = self.filter_meta_tokens(body)
        template = self.shell.environment.from_string(body, None, IPythonTemplate)
        vars = find_undeclared_variables(self.shell.environment.parse(body))
        return self.template_cls(
            body=body, template=template, vars=vars, markdown_renderer=self.markdown_renderer
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
        for key, displays in displays_by_key.items():
            value = self.get_value(key)

            if is_widget(value):
                if self.widgets.setdefault(key, value) is not value:
                    olds.append(self.widgets[key])
                    self.widgets[key] = value

                for display in displays:
                    value.observe(display.observe, "value")

        for old in olds:
            old.close()

    def post_run_cell(self, result):
        from IPython.display import display, Markdown

        id = self.get_id()
        if result.error_in_exec or result.error_before_exec:
            pass  # don't do anything when there are errors
        elif NO_SHOW.match(result.info.raw_cell):
            display(Markdown(f"<div hidden>\n\n{result.info.raw_cell}\n\n</div>"))
        elif CELL_MAGIC.match(result.info.raw_cell):
            pass
        else:
            self.displays[id] = self.weave_cell(result.info.raw_cell)
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
        if self.reactive:
            changed = set()

            for k, v in self.prior.items():
                y = self.get_value(k)
                if y is not v:
                    changed.add(k)

            for disp in self.displays.values():
                if changed.intersection(disp.vars):
                    ensure_future(disp.aupdate())

            if self.reactive:
                self.link_widgets()

    def update_displays(self):
        self.post_execute()


def load_ipython_extension(shell):
    __import__("nest_asyncio").apply()
    from .environment import load_ipython_extension

    load_ipython_extension(shell)
    if not shell.has_trait("weave"):
        shell.add_traits(
            weave=Instance(
                Weave, kw=dict(shell=shell, markdown_renderer=shell.tangle.parser), allow_none=True
            )
        )
    shell.events.register("pre_execute", shell.weave.pre_execute)
    shell.events.register("post_run_cell", shell.weave.post_run_cell)
    shell.events.register("post_execute", shell.weave.post_execute)


def unload_ipython_extension(shell):
    if shell.has_trait("weave"):
        for e in ["pre_execute", "post_run_cell", "post_execute"]:
            try:
                shell.events.unregister(e, getattr(shell.weave, e))
            except ValueError:
                pass
