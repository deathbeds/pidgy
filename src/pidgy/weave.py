from collections import defaultdict
from dataclasses import dataclass, field
from io import StringIO
from re import compile
from typing import ChainMap

from jinja2 import Environment, Template
from jinja2.meta import find_undeclared_variables
from markdown_it import MarkdownIt
from traitlets import Bool, Dict, Instance, Type

from .displays import IPythonMarkdown, TemplateDisplay, is_widget
from .environment import IPythonTemplate
from .pidgy import Extension

CELL_MAGIC = compile("^\s*%{2}\S")
NO_SHOW = compile(r"^\s*\r?\n")

URL = compile("^(http[s]|file)://")


class Weave(Extension):
    displays = Dict()
    prior = Dict()  # prior value to compare against when reacting to updates
    template_cls = Type(IPythonMarkdown, TemplateDisplay)
    markdown_renderer = Instance(MarkdownIt, args=())
    reactive = Bool(True)
    widgets = Dict()

    def weave_cell(self, body):
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


def load_ipython_extension(shell):
    from .environment import load_ipython_extension

    load_ipython_extension(shell)
    if not shell.has_trait("weave"):
        shell.add_traits(weave=Instance(Extension, allow_none=True))
    shell.weave = Weave(shell=shell, markdown_renderer=shell.tangle.parser)
    shell.weave.load_ipython_extension()


def unload_ipython_extension(shell):
    if shell.has_trait("weave"):
        shell.weave.unload_ipython_extension()
