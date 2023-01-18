from . import get_ipython, get_cell_id
from dataclasses import dataclass
import ast, types, dis
from contextlib import suppress


@dataclass
class Execution:
    id: str
    tokens: list = None
    py: str = None
    nodes: ast.AST = None
    bytecode: types.CodeType = None
    instructions: list[dis.Instruction] = None


class PidgyCompiler:
    def ast_parse(self, source, filename="<unknown>", symbol="exec"):
        get_ipython().current_execution.nodes = super().ast_parse(source, filename, symbol)
        return get_ipython().current_execution.nodes


def set_compiler_class(shell):
    if not issubclass(shell.compiler_class, PidgyCompiler):
        name = PidgyCompiler.__name__.replace("Compiler", shell.compiler_class.__name__)
        shell.compiler_class = type(name, (PidgyCompiler, shell.compiler_class), {})


def set_current_execution(shell):
    if shell.has_trait("current_execution"):
        id = get_cell_id(shell)
        if shell.current_execution:
            if shell.current_execution.id == id:
                return
        shell.current_execution = Execution(id)


def update_current_execution(lines):
    shell = get_ipython()
    set_current_execution(shell)
    return lines


def load_ipython_extension(shell):
    from traitlets import Instance

    set_compiler_class(shell)
    shell.compile = shell.compiler_class()
    shell.add_traits(current_execution=Instance(Execution, (None,)))
    with suppress(ValueError):
        shell.input_transformer_manager.cleanup_transforms.remove(update_current_execution)
    shell.input_transformer_manager.cleanup_transforms.insert(0, update_current_execution)


def unload_ipython_extension(shell):
    with suppress(ValueError):
        shell.input_transformer_manager.cleanup_transforms.remove(update_current_execution)

    shell.input_transformer_manager.cleanup_transforms.remove(update_current_execution, None)
    if issubclass(shell.compiler_class, PidgyCompiler):
        shell.compiler_class = shell.compiler_class.__mro__[2]
        shell.compile = shell.compiler_class()
