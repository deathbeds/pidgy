
# coding: utf-8

# In[1]:


from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell
from IPython.core.inputsplitter import IPythonInputSplitter
from IPython.core.compilerop import CachingCompiler
from IPython.utils.capture import capture_output
from textwrap import indent
import ast, sys
from json import load, loads
from dataclasses import dataclass, field
from nbformat import v4, NotebookNode, read
from nbformat.v4 import new_notebook
from json.scanner import py_make_scanner
from json.decoder import JSONObject, JSONDecoder, WHITESPACE, WHITESPACE_STR
from traitlets import Unicode, Any, default, Bool
from dataclasses import dataclass, field
from types import ModuleType
from pathlib import Path
from textwrap import dedent
from nbconvert.exporters.markdown import MarkdownExporter
from nbconvert.exporters.notebook import NotebookExporter
from pathlib import Path


# In[2]:


def identity(object, *_, **__): return object


# In[3]:


from json.decoder import JSONDecoder
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
        return NotebookNode(object), next
    


# In[4]:


def docify(NotebookNode): 
    return MarkdownExporter(config={'TemplateExporter': {'exclude_output': True}}).from_notebook_node(NotebookNode)[0]


# In[5]:


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
        return Module.from_notebook_node(load(file_stream, cls=Module.decoder), resources, **dict)
    
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


# In[6]:


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


# In[7]:


class Compile(AST):
    def from_notebook_node(Compile, nb, resources: dict=None, **dict):
        return Compile.compile(super().from_notebook_node(nb, resources, **dict), Compile.filename)


# In[8]:


def test():
    module = Partial().from_filename('SomeOutput.ipynb')
    assert isinstance(module, ModuleType)
    assert module.__complete__ is True


# In[9]:


from importlib.machinery import SourceFileLoader
class NotebookLoader(SourceFileLoader):
    EXTENSION_SUFFIXES = '.ipynb',
    
    def source_to_code(Loader, data, path):
        with __import__('io').BytesIO(data) as data:
            return Compile().from_file(data, filename=Loader.path, name=Loader.name)


# In[10]:


def capture(module):
    with capture_output() as output:
        try:
            super(type(Module), Module).exec_module(module)
            module.__complete__ = True
        except BaseException as Exception:
            module.__complete__ = Exception
    module.__output__ = output
    return module


# In[11]:


def capture(loader, module):
    with capture_output() as output:
        try:
            super(type(loader), loader).exec_module(module)
            module.__complete__ = True
        except BaseException as Exception:
            module.__complete__ = Exception
    module.__output__ = output
    return module


# In[12]:


class Partial(NotebookLoader):
    def exec_module(Module, module):
        return capture(Module, module)


# In[13]:


_NATIVE_HOOK = sys.path_hooks.copy()
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


# In[14]:


def load_ipython_extension(ip=None):
    update_hooks(Partial)
def unload_ipython_extension(ip=None):
    update_hooks()


# In[15]:


if 1 and __name__ ==  '__main__':
    __import__('doctest').testmod(verbose=2)
    load_ipython_extension()
    import rites
    get_ipython().system('jupyter nbconvert --to script rites.ipynb')

