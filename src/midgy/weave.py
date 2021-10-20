from dataclasses import dataclass, field
from re import compile
from typing import Any, Pattern

from jinja2 import Environment

_RE_BLANK_LINE = compile(r"^\s*\r?\n")


@dataclass
class Weave:
    shell: Any = field(
        default=None, metadata=dict(description="the current interactive shell")
    )
    environment: Environment = field(
        default_factory=Environment,
        metadata=dict(
            description="a templating environment for transcluding variables in narrative"
        ),
    )
    template: bool = field(
        default=True,
        metadata=dict(description="flag to render the output with or without jinja"),
    )
    asynch: bool = field(
        default=False,
        metadata=dict(description="a placeholder for future async support"),
    )
    reactive: bool = field(
        default=False,
        metadata=dict(description="reactive templates with the namespace."),
    )
    no_show: Pattern = field(
        default=_RE_BLANK_LINE,
        metadata=dict(description="the pattern for suppressing output"),
    )
    display_cls: type = field(default=None)
    debug: bool = field(default=False)

    def render(self, input):
        import builtins

        if self.template:
            input = self.environment.from_string(input).render(
                **{**vars(builtins), **self.shell.user_ns}
            )
        return input

    def display(self, input):
        from IPython.display import display, Markdown

        display(self.display_cls(self.render(input)))
        if self.debug:
            display(
                Markdown(
                    f"""tangled input: \n```python\n{self.shell.transform_cell(input)}\n```"""
                )
            )

    def post_run_cell(self, result):
        if not self.no_show.match(result.info.raw_cell):
            self.display(result.info.raw_cell)


def load_ipython_extension(shell):
    from IPython.display import Markdown

    from traitlets import Instance

    if not shell.has_trait("weave"):
        shell.add_traits(
            weave=Instance(Weave, kw=dict(display_cls=Markdown, shell=shell))
        )
    unload_ipython_extension(shell)
    shell.events.register("post_run_cell", shell.weave.post_run_cell)


def unload_ipython_extension(shell):
    from contextlib import suppress

    if shell.has_trait("weave"):
        with suppress(BaseException):
            shell.events.unregister("post_run_cell", shell.weave.post_run_cell)
