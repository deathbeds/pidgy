
# coding: utf-8

# # by *convention* Notebooks __import__
# 
# `rites` will install the proper actions to import notebooks from their JSON source to compiled Python bytecode with proper __traceback__s.

# # Decoding

# In[1]:


from json.decoder import JSONObject, JSONDecoder, WHITESPACE, WHITESPACE_STR    
from nbformat import NotebookNode
class LineNoDecoder(JSONDecoder):
    """A JSON Decoder to return a NotebookNode with lines numbers in the metadata.
    """
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


# # Compilation
# 
# Compilation occurs in the __3__ steps:
# 
# 1. Text is transformed into a valid source string.
# 2. The sources string is parsed into an abstract syntax tree
# 3. The abstract syntax compiles to valid bytecode 

# In[2]:


from IPython.core.compilerop import CachingCompiler
from dataclasses import dataclass, field

class Compiler(CachingCompiler):
    """{Shell} provides the IPython machinery to objects."""
    filename: str = '<Shell>'
    def __init__(self): 
        CachingCompiler.__init__(self)
        
    @property
    def ip(Compiler): 
        from IPython import get_ipython
        from IPython.core.interactiveshell import InteractiveShell
        return get_ipython() or InteractiveShell()
    
    def ast_transform(Compiler, node):
        for visitor in Compiler.ip.ast_transformers: 
            node = visitor.visit(node)
        return node
    
    @property
    def transform(Compiler): return Compiler.ip.input_transformer_manager.transform_cell

    def compile(Compiler, ast): 
        """Compile AST to bytecode using the an IPython compiler."""
        return (Compiler.ip and Compiler.ip.compile or CachingCompiler())(ast, Compiler.filename, 'exec')
            
    def ast_parse(Compiler, source, filename='<unknown>', symbol='exec', lineno=0): 
        return ast.increment_lineno(super().ast_parse(source, Compiler.filename, 'exec'), lineno)



# In[3]:


import ast, sys
from json import load, loads
from nbformat import NotebookNode, read, reads
from pathlib import Path
from nbconvert.exporters.markdown import MarkdownExporter
from nbconvert.exporters.notebook import NotebookExporter


# In[4]:


@dataclass
class Code(NotebookExporter, Compiler):
    """An exporter than returns a NotebookNode with the InputSplitter transforms applied.
    
    >>> assert type(Code().from_filename('rites.ipynb')) is NotebookNode"""
    filename: str = '<module exporter>'
    name: str = '__main__'
    decoder: type = LineNoDecoder
        
    def __post_init__(self): NotebookExporter.__init__(self) or Compiler.__init__(self)
            
    def from_file(Code,file_stream, resources=None, **dict): 
        for str in ('name', 'filename'): setattr(Code, str, dict.pop(str, getattr(Code, str)))
        return Code.from_notebook_node(
            NotebookNode(**load(file_stream, cls=Code.decoder)), resources, **dict)
    
    def from_filename(Code,  filename, resources=None, **dict):
        Code.filename, Code.name = filename, Path(filename).stem
        return super().from_filename(filename, resources, **dict)

    def from_notebook_node(Code, nb, resources=None, **dict): 
        for cell in nb['cells']:
            if cell['cell_type'] == 'code':
                cell.source = Code.from_code_cell(cell, **dict)
        return nb
    
    def from_code_cell(Code, cell, **dict):  return Code.transform(cell['source'])


# In[5]:


class AST(Code):
    """An exporter than returns parsed ast.
    
    >>> assert type(AST().from_filename('rites.ipynb')) is ast.Module"""
    def from_notebook_node(AST, nb: NotebookNode, resource: dict=None, **dict):         
        return AST.ast_transform(ast.fix_missing_locations(ast.Module(body=sum((
            AST.ast_parse(
                AST.from_code_cell(cell, **dict), lineno=cell['metadata'].get('lineno', 1)
            ).body for cell in nb.cells if cell['cell_type']=='code'
        ), []))))


# In[6]:


class Compile(AST):
    """An exporter than returns compiled bytecode
    
    >>> assert Compile().from_filename('rites.ipynb')"""        
    def from_notebook_node(Compile, nb, resources: dict=None, **dict):
        return Compile.compile(super().from_notebook_node(nb, resources, **dict))


# # Import System
# 
# `rites` will exploit as much of the Python import system as it can.

# In[7]:


from importlib.machinery import SourceFileLoader
class NotebookLoader(SourceFileLoader):
    """A SourceFileLoader for notebooks that provides line number debugginer in the JSON source."""
    EXTENSION_SUFFIXES = '.ipynb',
    def exec_module(Loader, module):
        module.__doc__ = docify(reads(Loader.get_source(Loader.name), 4))
        return super().exec_module(module)
    def source_to_code(Loader, data, path):
        with __import__('io').BytesIO(data) as stream:
            return Compile().from_file(stream, filename=Loader.path, name=Loader.name)


# ## Partial Loading
# 
# A notebook may be a complete, or yet to be complete concept.  Unlike normal source code, notebooks are comprised of cells 
# or miniature programs that may interact with other cells.  It is plausible that some code may evaluate before other code fails.  `rites` allows notebooks to partially evalue.  Each module contains `module.__complete__` to identify the loading
# state of the notebook.

# In[8]:


class Partial(NotebookLoader):    
    """A SourceFileLoader that will always work because it catches output and error.
    
    """
    def exec_module(Module, module):
        from IPython.utils.capture import capture_output
        with capture_output(stdout=False, stderr=False) as output:
            super(type(Module), Module).exec_module(module)
            try: module.__complete__ = True
            except BaseException as Exception: module.__complete__ = Exception
            finally: module.__output__ = output
        return module


# In[9]:


_NATIVE_HOOK = sys.path_hooks
def update_hooks(loader=None):
    """Update the sys.meta_paths with the PartialLoader.
    
    """
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

# In[10]:


def load_ipython_extension(ip=None): update_hooks(Partial)
def unload_ipython_extension(ip=None): update_hooks()


# ## Utilities

# In[11]:


def docify(NotebookNode): 
        """Create a markdown of the notebook input."""
        return md(MarkdownExporter(config={'TemplateExporter': {'exclude_output': True}}).from_notebook_node(NotebookNode)[0])
    
class md(str): 
    """A string with a markdown repr."""
    def _repr_markdown_(self): return str(self)


# ### Force the docstring for rites itself.

# In[12]:


class Test(__import__('unittest').TestCase): 
    def setUp(Test):
        from nbformat import write, v4
        load_ipython_extension()
        with open('test_rites.ipynb', 'w') as file:
            write(v4.new_notebook(cells=[
                v4.new_code_cell("test = 42")
            ]), file)
            
    def runTest(Test):
        import test_rites
        assert test_rites.__file__.endswith('.ipynb')
        assert test_rites.test is 42
        assert isinstance(test_rites, __import__('types').ModuleType)
        
    def tearDown(Test):
        get_ipython().run_line_magic('rm', 'test_rites.ipynb')
        unload_ipython_extension()


# # Developer

# In[ ]:


if __name__ ==  '__main__':
    del __doc__
    __import__('doctest').testmod(verbose=2)
    __import__('unittest').TextTestRunner().run(Test())
    get_ipython().system('jupyter nbconvert --to script rites.ipynb')

__doc__ = docify(reads(Path(
        globals().get('__file__', 'rites.ipynb')).with_suffix('.ipynb').read_text(), 4))

