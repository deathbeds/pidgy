
# coding: utf-8

# ##### The First Convention
# # Notebooks __import__
# 
# A notebook that will __import__ is a necessary condition for a notebook to Restart and Run All.  The tool is meant to be using with IPython.

# In[1]:


from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell
from IPython.core.inputsplitter import IPythonInputSplitter
from IPython.core.compilerop import CachingCompiler
from IPython.utils.capture import capture_output


# In[2]:


from textwrap import indent
import ast, sys
from json import load, loads
from dataclasses import dataclass, field
from nbformat import v4, NotebookNode, read
from nbformat.v4 import new_notebook
from traitlets import Unicode, Any, default, Bool
from dataclasses import dataclass, field
from types import ModuleType
from pathlib import Path
from textwrap import dedent
from nbconvert.exporters.markdown import MarkdownExporter
from nbconvert.exporters.notebook import NotebookExporter
from pathlib import Path


# In[3]:


def identity(object, *_, **__): return object


# `rites` will provide a valid traceback to the source file, if the file is unchanged.    A custom JSONDecoder will track the line numbers in the source file, they are passed to the cell metadata. _There is no nbformat check yet._

# In[ ]:


from json.scanner import py_make_scanner    
from json.decoder import JSONObject, JSONDecoder, WHITESPACE, WHITESPACE_STR
from nbformat import v4, NotebookNode, read, reads
from nbformat.v4 import new_notebook
class LineNoDecoder(JSONDecoder):
    """A JSON Decoder to return a NotebookNode with lines numbers in the metadata.
    
    """
    def __init__(self, *, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, strict=True, object_pairs_hook=None):
        super().__init__(object_hook=object_hook, parse_float=parse_float, parse_int=parse_int, parse_constant=parse_constant, strict=strict, 
                         object_pairs_hook=object_pairs_hook)
        self.parse_object = self.object
        self.scan_once = py_make_scanner(self)
        
    def object(self, s_and_end, strict, scan_once, object_hook, object_pairs_hook, memo=None, _w=WHITESPACE.match, _ws=WHITESPACE_STR):
        object, next = JSONObject(s_and_end, strict, scan_once, object_hook, object_pairs_hook, memo=memo, _w=_w, _ws=_ws)

        if 'cell_type' in object: object['metadata'].update(
            {'lineno':  len(s_and_end[0][:next].rsplit('"source":', 1)[0].splitlines())})
            
        for key in ('source', 'text'): 
            if key in object: object[key] = ''.join(object[key])
        return object, next
    


# In[ ]:


@dataclass
class Code(NotebookExporter):
    filename: str = '<module exporter>'
    name: str = '__main__'
    ip: bool = field(default_factory=get_ipython)
    decoder: type = LineNoDecoder
        
    __post_init__ = NotebookExporter.__init__
            
    def from_file(Module,file_stream, resources=None, **dict): 
        for str in ('name', 'filename'):
            setattr(Compile, str, dict.pop(str, getattr(Compile, str)))
        return Module.from_notebook_node(
            NotebookNode(load(file_stream, cls=Module.decoder)), resources, **dict)
    
    def from_filename(Module,  filename, resources=None, **dict):
        Module.filename, Module.name = filename, Path(filename).stem
        return super().from_filename(filename, resources, **dict)

    
    @property
    def compiler(Code): return Code.ip.compile if Code.ip else compile

    @property
    def parser(Code): return Code.compiler.ast_parse if Code.ip else ast.parse
    
    @property
    def transform(Code): 
        return Code.ip.input_transformer_manager.transform_cell if Code.ip else identity
    
    def compile(Loader, data, path): return Loader.compiler(data, path, 'exec')
    
    def parse(Module, source, *, lineno=0): 
        return ast.increment_lineno(Module.parser(source, Module.filename, 'exec'), lineno)
    
    def from_code_cell(Module, cell, **dict):
        if cell['cell_type'] == 'code': return Module.transform(cell['source'])
        
        


# In[ ]:


class AST(Code):
    def from_notebook_node(AST, nb: NotebookNode, resource: dict=None, **dict):         
        module = ast.Module(body=[])
        for cell in nb.cells:
            nodes = AST.from_code_cell(cell, **dict)
            nodes and module.body.extend(nodes.body)
        return ast.fix_missing_locations(module)
    
    def from_code_cell(Module, cell, **dict):
        code = super().from_code_cell(cell)
        if code:
            return Module.parse(code, lineno=cell['metadata'].get('lineno', 1))


# In[ ]:


class Compile(AST):
    def from_notebook_node(Compile, nb, resources: dict=None, **dict):
        return Compile.compile(super().from_notebook_node(nb, resources, **dict), Compile.filename)


# In[ ]:


def test():
    module = Partial().from_filename('SomeOutput.ipynb')
    assert isinstance(module, ModuleType)
    assert module.__complete__ is True


# In[ ]:


from importlib.machinery import SourceFileLoader
class NotebookLoader(SourceFileLoader):
    EXTENSION_SUFFIXES = '.ipynb',
    def exec_module(Loader, module):
        module.__doc__ = docify(reads(Loader.get_source(Loader.name), 4))
        return super().exec_module(module)
    def source_to_code(Loader, data, path):
        with __import__('io').BytesIO(data) as data:
            return Compile().from_file(data, filename=Loader.path, name=Loader.name)


# In[ ]:


def capture(Module, module):
    with capture_output() as output:
        try:
            super(type(Module), Module).exec_module(module)
            module.__complete__ = True
        except BaseException as Exception:
            module.__complete__ = Exception
    module.__output__ = output
    return module


# In[ ]:


class Partial(NotebookLoader):
    def exec_module(Module, module): return capture(Module, module)            


# In[ ]:


_NATIVE_HOOK = sys.path_hooks
def update_hooks(loader=None):
    global _NATIVE_HOOK
    from importlib.machinery import FileFinder
    if loader:
        for i, hook in enumerate(sys.path_hooks):
            closure = getattr(hook, '__closure__', None)
            if closure and closure[0].cell_contents is FileFinder:
                sys.path_hooks[i] = FileFinder.path_hook(
                    (loader, list(loader.EXTENSION_SUFFIXES)), *closure[1].cell_contents)
    else: sys.path_hooks = _NATIVE_HOOK
    sys.path_importer_cache.clear()


# In[ ]:


def load_ipython_extension(ip=None):
    update_hooks(Partial)
def unload_ipython_extension(ip=None):
    update_hooks()


# In[ ]:


class md(str): 
    """A string with a markdown repr."""
    def _repr_markdown_(self): return str(self)


# In[ ]:


def docify(NotebookNode): 
        """Create a markdown of the notebook input."""
        return md(MarkdownExporter(config={'TemplateExporter': {'exclude_output': True}}).from_notebook_node(NotebookNode)[0])


# Force the docstring for rites itself.

# In[ ]:


with (
    Path(
        globals()
        .get('__file__', 'rites.ipynb')
    ).with_suffix('.ipynb')
    .open()
) as f: __doc__ = docify(read(f, 4))


# In[ ]:


if 1 and __name__ ==  '__main__':
    __import__('doctest').testmod(verbose=2)
    load_ipython_extension()
    import rites
    get_ipython().system('jupyter nbconvert --to script rites.ipynb')

