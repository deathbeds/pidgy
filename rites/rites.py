
# coding: utf-8

# In[1]:


from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell
from IPython.core.inputsplitter import IPythonInputSplitter
from IPython.core.compilerop import CachingCompiler
from IPython.utils.capture import capture_output
from textwrap import indent
import ast, sys
from json import load
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
class Module(NotebookExporter):
    filename: str = '<module exporter>'
    name: str = '__main__'
    ip: bool = get_ipython()
    
    def __post_init__(self): NotebookExporter.__init__(self)
        
    def from_filename(Module,  filename, resources=None, **dict):
        Module.filename, Module.name = filename, __import__('pathlib').Path(filename).stem
        return super().from_filename(filename, resources, **dict)
    
    def from_file(Module,  file_stream, resources=None, **dict): return Module.from_notebook_node(
        new_notebook(**load(file_stream, cls=LineNoDecoder)), resources)

    def from_notebook_node(Module, nb: NotebookNode, resource: dict=None, *, module: ModuleType=None) -> ModuleType:            
        if module is None: module = ModuleType(Module.name)
        
        module.__doc__ = docify(nb)
        with capture_output() as output:
            for cell in nb.cells:
                if cell['cell_type'] == 'code':
                    try: eval(Module.compile(
                        cell['source'], lineno=cell['metadata'].get('lineno', 1), module=module),
                        *[module.__dict__]*2)
                    except BaseException as Exception: 
                        module.__complete__ = Exception
                        break
            else: module.__complete__ = True
        module.__output__ = output
        return module   
    
    @property
    def parse(Module): return Module.ip.compile.ast_parse if Module.ip else ast.parse
    
    def transform(Module, source): 
        if Module.ip:
            return Module.ip.input_transformer_manager.transform_cell(
                get_ipython().input_transformer_manager.transform_cell(source))
        return identity
    
    def compile(Module, source, *, lineno=0, module=None): return compile(
        ast.increment_lineno(Module.parse(Module.transform(source), Module.filename, 'exec'), lineno), 
        Module.filename, 'exec')


# In[6]:


def test():
    module = Module().from_filename('SomeOutput.ipynb')
    assert isinstance(module, ModuleType)
    assert module.__complete__ is True


# In[7]:


from importlib.machinery import SourceFileLoader
class NotebookLoader(SourceFileLoader):
    EXTENSION_SUFFIXES = '.ipynb',
    def exec_module(Notebook, module): return module.__dict__.update(
        vars(Module().from_filename(Notebook.path, module=module)))


# In[8]:


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


# In[9]:


def load_ipython_extension(ip=None):
    update_hooks(NotebookLoader)
def unload_ipython_extension(ip=None):
    update_hooks()


# In[10]:


if 1 and __name__ ==  '__main__':
    __import__('doctest').testmod(verbose=2)
    load_ipython_extension()
    import testing
    get_ipython().system('jupyter nbconvert --to script rites.ipynb')

