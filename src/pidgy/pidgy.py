import ast
import dataclasses
import dis
import types
from ast import NodeTransformer
from importlib import import_module

import IPython
from traitlets import Any, Bool, CUnicode, Dict, HasTraits, Instance, List, default

from . import get_ipython

MAGICS = {"line", "line_cell", "cell"}
TRANSFORMS = {"cleanup_transforms"}


class Extension(HasTraits):
    from . import IS_IPY

    IS_IPY = True

    alias = CUnicode(allow_none=True)
    shell = Instance("IPython.InteractiveShell")
    enabled = Bool(True)

    def __init_subclass__(cls, alias=None, **kwargs):
        if alias:
            cls.alias = CUnicode(default=alias)
        super().__init_subclass__(**kwargs)

    def load_ipython_extension(self):
        # if self.register:
        #     # register a trait with a specific name on the current shell
        #     if not self.shell.has_trait(self.alias):
        #         self.shell.add_traits(**{self.alias: Instance(type(self))})

        #     # set the attribute on the shell
        #     setattr(self.shell, self.alias, self)

        # register any methods corresponding the shell events callbacks names
        for event in self.shell.events.callbacks:
            property = getattr(self, event, None)
            if property is not None:
                self.shell.events.register(event, property)

        vars = set(dir(self))

        for magic in set(MAGICS).intersection(vars):
            self.shell.register_magic_function(getattr(self, magic), magic, self.alias)

        if isinstance(self, NodeTransformer):
            self.shell.ast_transformers.append(self)

        for transform in TRANSFORMS.intersection(vars):
            getattr(self.shell.input_transformer_manager, transform).insert(
                0, getattr(self, transform)
            )

        return self

    def unload_ipython_extension(self):
        for event, callers in self.shell.events.callbacks.items():
            this = type(self)
            if this:
                for caller in callers:
                    if issubclass(type(caller.__self__), Extension):
                        self.shell.events.unregister(event, caller)

        vars = set(dir(self))

        if isinstance(self, NodeTransformer):
            self.shell.ast_transformers = [x for x in self.shell.ast_transformers if x is not self]

        for transform in TRANSFORMS.intersection(vars):
            f = getattr(type(self), transform)
            ts = getattr(self.shell.input_transformer_manager, transform)

            transforms = [t for t in ts if getattr(type(t), transform, None) is not f]
            setattr(self.shell.input_transformer_manager, transform, transforms)

        return self


class PidgyCompiler:
    def ast_parse(self, source, filename="<unknown>", symbol="exec"):
        get_ipython().pidgy.current_execution.nodes = super().ast_parse(source, filename, symbol)
        return get_ipython().pidgy.current_execution.nodes


class Pidgy(HasTraits):
    extensions = List()
    current_execution = Any()


def pidgy_record_py(lines):
    get_ipython().pidgy.current_execution.py = "".join(lines)
    return lines


def set_compiler_class(shell):
    name = PidgyCompiler.__name__.replace("Compiler", shell.compiler_class.__name__)
    shell.compiler_class = type(name, (PidgyCompiler, shell.compiler_class), {})


def load_ipython_extension(shell):
    if not shell.has_trait("pidgy)"):
        shell.add_traits(pidgy=Instance(Pidgy, ()))

    shell.input_transformers_post.append(pidgy_record_py)
    set_compiler_class(shell)
    shell.compile = shell.compiler_class()


def unload_ipython_extension(shell):
    try:
        shell.input_transformers_post.remove(pidgy_record_py)
    except ValueError:
        pass

    if issubclass(shell.compiler_class, PidgyCompiler):
        shell.compiler_class = shell.compiler_class.__mro__[2]
        shell.compile = shell.compiler_class()
