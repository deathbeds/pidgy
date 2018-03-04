
# coding: utf-8

# ##### The First Convention
# # Notebooks __import__
# 
# `rites` will install the proper actions to import notebooks from their JSON source to compiled Python bytecode with proper __traceback__s.

# # Parsing

# `LineNoDecoder` is a `JSONDecoder` that updates the cell metadata with line numbers.

# In[1]:


from json.decoder import JSONObject, JSONDecoder, WHITESPACE, WHITESPACE_STR    
from nbformat import NotebookNode
class LineNoDecoder(JSONDecoder):
    """A JSON Decoder to return a NotebookNode with lines numbers in the metadata."""
    def __init__(self, *, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, strict=True, object_pairs_hook=None):
        from json.scanner import py_make_scanner    
        super().__init__(object_hook=object_hook, parse_float=parse_float, parse_int=parse_int, parse_constant=parse_constant, strict=strict, 
                         object_pairs_hook=object_pairs_hook)
        self.parse_object = self.object
        self.scan_once = py_make_scanner(self)
        
    def object(
        self, 
        s_and_end, 
        strict, scan_once, object_hook, object_pairs_hook, memo=None, _w=WHITESPACE.match, _ws=WHITESPACE_STR
    ) -> (NotebookNode, int):
        object, next = JSONObject(s_and_end, strict, scan_once, object_hook, object_pairs_hook, memo=memo, _w=_w, _ws=_ws)

        if 'cell_type' in object: object['metadata'].update(
            {'lineno':  len(s_and_end[0][:next].rsplit('"source":', 1)[0].splitlines())})
            
        for key in ('source', 'text'): 
            if key in object: object[key] = ''.join(object[key])
        return NotebookNode(object), next


# `Shell` is reusable class that provides the attributes to:
# 
# * `transform` text to source text
# * `parse` source text to `ast`
# * `compile` `ast` to `bytecode`

# In[2]:


from dataclasses import dataclass, field

@dataclass
class Shell:
    filename: str = '<rites.rites.Shell>'
    @property
    def ip(Shell): 
        from IPython import get_ipython
        from IPython.core.interactiveshell import InteractiveShell
        return get_ipython() or InteractiveShell()
    
    @property
    def transform(Shell): return Shell.ip.input_transformer_manager.transform_cell
    
    def compile(Shell, data): return Shell.ip.compile(data, Shell.filename, 'exec')
    
    def parse(Shell, source, *, lineno=0): return ast.increment_lineno(
        Shell.ip.compile.ast_parse(Shell.transform(source), Shell.filename, 'exec'), lineno)


# In[3]:


import ast, sys
from json import load, loads
from nbformat import NotebookNode, read, reads
from dataclasses import dataclass, field
from pathlib import Path
from nbconvert.exporters.markdown import MarkdownExporter
from nbconvert.exporters.notebook import NotebookExporter


# # Compilation
# 
# Compilation occurs in the __3__ steps:
# 
# 1. Text is transformed into a valid source string.
# 2. The sources string is parsed into an abstract syntax tree
# 3. The abstract syntax compiles to valid bytecode 

# In[4]:


@dataclass
class Code(NotebookExporter, Shell):
    """>>> assert type(Code().from_filename('rites.ipynb')) is NotebookNode"""
    filename: str = '<module exporter>'
    name: str = '__main__'
    decoder: type = LineNoDecoder
        
    __post_init__ = NotebookExporter.__init__
            
    def from_file(Code,file_stream, resources=None, **dict): 
        for str in ('name', 'filename'):
            setattr(Code, str, dict.pop(str, getattr(Code, str)))
        return Code.from_notebook_node(
            NotebookNode(**load(file_stream, cls=Code.decoder)), resources)
    
    def from_filename(Code,  filename, resources=None, **dict):
        Code.filename, Code.name = filename, Path(filename).stem
        return super().from_filename(filename, resources, **dict)
    
    def from_notebook_node(code, nb, resources=None, **dict): return nb


# In[5]:


class AST(Code):
    """>>> assert type(AST().from_filename('rites.ipynb')) is ast.Module"""
    def from_notebook_node(AST, nb: NotebookNode, resource: dict=None, **dict):         
        module = ast.Module(body=[])
        for cell in nb.cells: 
            if cell['cell_type']=='code':
                module.body.extend(AST.from_code_cell(cell, **dict).body)
        return ast.fix_missing_locations(module)
            
    def from_code_cell(AST, cell, **dict): return AST.parse(
        cell['source'], lineno=cell['metadata'].get('lineno', 1))


# In[6]:


class Compile(AST):
    """>>> assert Compile().from_filename('rites.ipynb')"""
    def from_notebook_node(Compile, nb, resources: dict=None, **dict):
        return Compile.compile(super().from_notebook_node(nb, resources, **dict))


# # Import System
# 
# `rites` will exploit as much of the Python import system as it can.

# In[7]:


from importlib.machinery import SourceFileLoader
class NotebookLoader(SourceFileLoader):
    EXTENSION_SUFFIXES = '.ipynb',
    def exec_module(Loader, module):
        module.__doc__ = docify(reads(Loader.get_source(Loader.name), 4))
        return super().exec_module(module)
    def source_to_code(Loader, data, path):
        with __import__('io').BytesIO(data) as data:
            return Compile().from_file(data, filename=Loader.path, name=Loader.name)


# ## Partial Loading
# 
# A notebook may be a complete, or yet to be complete concept.  Unlike normal source code, notebooks are comprised of cells 
# or miniature programs that may interact with other cells.  It is plausible that some code may evaluate before other code fails.  `rites` allows notebooks to partially evalue.  Each module contains `module.__complete__` to identify the loading
# state of the notebook.

# In[8]:


class Partial(NotebookLoader):    
    def exec_module(Module, module):
        from IPython.utils.capture import capture_output
        with capture_output() as output:
            try:
                super(type(Module), Module).exec_module(module)
                module.__complete__ = True
            except BaseException as Exception:
                module.__complete__ = Exception
        module.__output__ = output
        return module


# In[9]:


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


# # IPython Extensions

# In[11]:


def load_ipython_extension(ip=None): update_hooks(Partial)
def unload_ipython_extension(ip=None): update_hooks()


# ## Utilities

# In[20]:


def docify(NotebookNode): 
        """Create a markdown of the notebook input."""
        return md(MarkdownExporter(config={'TemplateExporter': {'exclude_output': True}}).from_notebook_node(NotebookNode)[0])
    
class md(str): 
    """A string with a markdown repr."""
    def _repr_markdown_(self): return str(self)


# ### Force the docstring for rites itself.

# In[21]:


with (
    Path(
        globals()
        .get('__file__', 'rites.ipynb')
    ).with_suffix('.ipynb')
    .open()
) as f: __doc__ = docify(read(f, 4))


# # Developer

# In[ ]:


if 1 and __name__ ==  '__main__':
    __import__('doctest').testmod(verbose=2)
    load_ipython_extension()
    import rites
    get_ipython().system('jupyter nbconvert --to script rites.ipynb')

