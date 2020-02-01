## The `pidgin` implementation
### An `IPython` extension.

    def load_ipython_extension(shell):
        """
The `pidgin` `load_ipython_extension`'s primary function transforms the `jupyter`
`notebook`s into a literate computing interfaces.
`markdown` becomes the primary plain-text format for submitting code,
and the `markdown` is translated to `python` source code
before compilation.
The implementation configures the appropriate
features of the `IPython.InteractiveShell` to accomodate
the interactive literate programming experience.

In this section, we'll implement a `shell.input_transformer_manager`
that handles the logical translation of `markdown` to `python`.
The translation maintains the source line numbers and 
normalizes the narrative relative to the source code.  Consequently,
introduces new syntaxes at the interfaces between `markdown and python`.

        """
        pidgin_transformer = PidginTransformer()        
        shell.input_transformer_manager = pidgin_transformer
        
        """
`IPython` provides configurable interactive `shell` properties.  Some of the configurable properties
control how `input` code is translated into valid source code. 
The `pidgin` translation is managed by a custom `IPython.core.inputtransformer2.TransformerManager`.
        
        """"""
        >>> shell.input_transformer_manager
        <...PidginTransformer object...>
        
        """"""

The `shell.input_transformer_manager` applies string transformations to clean up the `input`
to be valid `python`.  There are three stages of line of transforms.

1. Cleanup transforms that operate on the entire cell `input`.

        """"""
        >>> shell.input_transformers_cleanup
        [<...leading_empty_lines...>, <...leading_indent...>, <...PromptStripper...>, ...]
        
        """"""
        
2. Line transforms that are applied the cell `input` with split lines. 
This is where `IPython` introduces their bespoke cell magic syntaxes.
        
        """"""
        >>> shell.input_transformer_manager.line_transforms
        [...<...cell_magic...>...]
        
        """"""
        
3. Token transformers that look for specific tokens at the like level.  `IPython`'s default
behavior introduces new symbols into the programming language.

        """"""
        >>> shell.input_transformer_manager.token_transformers
        [<...MagicAssign...SystemAssign...EscapedCommand...HelpEnd...>]
        
        """"""

After all of the `input` transformations are complete, the `input` should be valid source that `ast.parse, compile or shell.compile` 
may accept.

        """"""
        >>> shell.ast_transformers
        [...]
        
        """

        if not any(x for x in shell.ast_transformers if isinstance(x, ReturnYield)):
            shell.ast_transformers.append(ReturnYield())



    class PidginTransformer(IPython.core.inputtransformer2.TransformerManager):
        def pidgin_transform(self, cell: str) -> str: 
            tokens = self.tokenizer.parse(''.join(cell))
            return self.tokenizer.untokenize(tokens)
        
        def pidgin_cleanup(self, cell: str) -> list: 
            return self.pidgin_transform(cell).splitlines(True)
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.tokenizer = Tokenizer()
            self.cleanup_transforms.insert(0, self.pidgin_cleanup)
            self.line_transforms.append(demojize)

        def pidgin_magic(self, *text): 
            """Expand the text to tokens to tokens and 
            compact as a formatted `"python"` code."""
            return IPython.display.Code(self.pidgin_transform(''.join(text)), language='python')
        



    import ast
    class ReturnYield(ast.NodeTransformer):
        def visit_FunctionDef(self, node): return node
        visit_AsyncFunctionDef = visit_FunctionDef
        def visit_Return(self, node):
            replace = ast.parse('''__import__('IPython').display.display()''').body[0]
            replace.value.args = node.value.elts if isinstance(node.value, ast.Tuple) else [node.value]
            return ast.copy_location(replace, node)

        def visit_Expr(self, node):
            if isinstance(node.value, (ast.Yield, ast.YieldFrom)):  return ast.copy_location(self.visit_Return(node.value), node)
            return node
        
        visit_Expression = visit_Expr



    import mistune as markdown, textwrap, __main__, IPython, typing, re, IPython, nbconvert, ipykernel, doctest, ast
    __all__ = 'pidgin',



    class Tokenizer(markdown.BlockLexer):
            """
### Tokenizer

<details>
<summary>Tokenize `input` text into `"code" and not "code"` tokens that will be translated into valid `python` source.</summary>
        
            """
            class grammar_class(markdown.BlockGrammar):
                doctest = doctest.DocTestParser._EXAMPLE_RE

            def parse(self, text: str, default_rules=None) -> typing.List[dict]:
                if not self.depth: self.tokens = []
                with self: tokens = super().parse(whiten(text), default_rules)
                if not self.depth: tokens = self.compact(text, tokens)
                return tokens

            def parse_doctest(self, m): self.tokens.append({'type': 'paragraph', 'text': m.group(0)})

            def parse_fences(self, m):
                if m.group(2): self.tokens.append({'type': 'paragraph', 'text': m.group(0)})
                else: super().parse_fences(m)

            def parse_hrule(self, m):
                self.tokens.append({'type': 'hrule', 'text': m.group(0)})

            def compact(self, text, tokens):
                """Combine non-code tokens into contiguous blocks."""
                compacted = []
                while tokens:
                    token = tokens.pop(0)
                    if 'text' not in token: continue
                    else: 
                        if not token['text'].strip(): continue
                        block, body = token['text'].splitlines(), ""
                    while block:
                        line = block.pop(0)
                        if line:
                            before, line, text = text.partition(line)
                            body += before + line
                    if token['type']=='code':
                        compacted.append({'type': 'code', 'lang': None, 'text': body})
                    else:
                        if compacted and compacted[-1]['type'] == 'paragraph':
                            compacted[-1]['text'] += body
                        else: compacted.append({'type': 'paragraph', 'text': body})
                if compacted and compacted[-1]['type'] == 'paragraph':
                    compacted[-1]['text'] += text
                elif text.strip():
                    compacted.append({'type': 'paragraph', 'text': text})
                return compacted

            depth = 0
            def __enter__(self): self.depth += 1
            def __exit__(self, *e): self.depth -= 1

            def untokenize(self, tokens: τ.List[dict], source: str = """""", last: int =0) -> str:
                INDENT = indent = base_indent(tokens) or 4
                for i, token in enumerate(tokens):
                    object = token['text']
                    if token and token['type'] == 'code':
                        if object.lstrip().startswith(FENCE):

                            object = ''.join(''.join(object.partition(FENCE)[::2]).rpartition(FENCE)[::2])
                            indent = INDENT + num_first_indent(object)
                            object = textwrap.indent(object, INDENT*SPACE)

                        if object.lstrip().startswith(MAGIC):  ...
                        else: indent = num_last_indent(object)
                    elif not object: ...
                    else:
                        object = textwrap.indent(object, indent*SPACE)
                        for next in tokens[i+1:]:
                            if next['type'] == 'code':
                                next = num_first_indent(next['text'])
                                break
                        else: next = indent       
                        Δ = max(next-indent, 0)

                        if not Δ and source.rstrip().rstrip(CONTINUATION).endswith(COLON): 
                            Δ += 4

                        spaces = num_whitespace(object)
                        "what if the spaces are ling enough"
                        object = object[:spaces] + Δ*SPACE+ object[spaces:]
                        if not source.rstrip().rstrip(CONTINUATION).endswith(QUOTES): 
                            object = quote(object)
                    source += object

                for token in reversed(tokens):
                    if token['text'].strip():
                        if token['type'] != 'code': 
                            source = source.rstrip() + SEMI
                        break

                return source 
            
    for x in "default_rules footnote_rules list_rules".split():
        setattr(Tokenizer, x, list(getattr(Tokenizer, x)))
        getattr(Tokenizer, x).insert(getattr(Tokenizer, x).index('block_code'), 'doctest')
        
    ...
    """
</details>&nbsp;

    """
    pidgin = PidginTransformer()


A potential outcome of a `pidgin` program is reusable code. 

Import pidgin notebooks as modules.


    class PidginLoader(__import__('importnb').Notebook): 
        extensions = ".ipynb .md.ipynb".split()
        def code(self, str): return ''.join(pidgin.transform_cell(str))



    class PidginPreprocessor(nbconvert.preprocessors.Preprocessor):
        def preprocess_cell(self, cell, resources, index, ):
            if cell['cell_type'] == 'code':
                cell['source'] = pidgin_transformer.transform_cell(''.join(cell['source']))
            return cell, resources


The shell is the application either jupyterlab or jupyter notebook, the kernel determines the programming language.  Below we design a just jupyter kernel that can be installed using 

    !pidgin kernel install


    class PidginInteractiveShell(IPython.InteractiveShell):
        """Configure a native `pidgin` `IPython.InteractiveShell`"""
    PidginInteractiveShell.input_transformer_manager.default_value = PidginTransformer
    PidginInteractiveShell.enable_html_pager.default_value = True

    class PidginKernelApp(ipykernel.kernelapp.IPKernelApp): 
        """Configure a native `pidgin` `__import__('ipykernel').kernelapp.IPKernelApp"""
    PidginKernelApp.shell.default_value = PidginInteractiveShell







![svg](paper.md_files/paper.md_4_0.svg)




## programming in `markdown and python` 
[📓](imports.ipynb)


    def load_ipython_extension(shell):
        """
The `pidgin` `load_ipython_extension`'s primary function transforms the `jupyter`
`notebook`s into a literate computing interfaces.
`markdown` becomes the primary plain-text format for submitting code,
and the `markdown` is translated to `python` source code
before compilation.
The implementation configures the appropriate
features of the `IPython.InteractiveShell` to accomodate
the interactive literate programming experience.

In this section, we'll implement a `shell.input_transformer_manager`
that handles the logical translation of `markdown` to `python`.
The translation maintains the source line numbers and 
normalizes the narrative relative to the source code.  Consequently,
introduces new syntaxes at the interfaces between `markdown and python`.

        """
        pidgin_transformer = PidginTransformer()        
        shell.input_transformer_manager = pidgin_transformer
        
        """
`IPython` provides configurable interactive `shell` properties.  Some of the configurable properties
control how `input` code is translated into valid source code. 
The `pidgin` translation is managed by a custom `IPython.core.inputtransformer2.TransformerManager`.
        
        """"""
        >>> shell.input_transformer_manager
        <...PidginTransformer object...>
        
        """"""

The `shell.input_transformer_manager` applies string transformations to clean up the `input`
to be valid `python`.  There are three stages of line of transforms.

1. Cleanup transforms that operate on the entire cell `input`.

        """"""
        >>> shell.input_transformers_cleanup
        [<...leading_empty_lines...>, <...leading_indent...>, <...PromptStripper...>, ...]
        
        """"""
        
2. Line transforms that are applied the cell `input` with split lines. 
This is where `IPython` introduces their bespoke cell magic syntaxes.
        
        """"""
        >>> shell.input_transformer_manager.line_transforms
        [...<...cell_magic...>...]
        
        """"""
        
3. Token transformers that look for specific tokens at the like level.  `IPython`'s default
behavior introduces new symbols into the programming language.

        """"""
        >>> shell.input_transformer_manager.token_transformers
        [<...MagicAssign...SystemAssign...EscapedCommand...HelpEnd...>]
        
        """"""

After all of the `input` transformations are complete, the `input` should be valid source that `ast.parse, compile or shell.compile` 
may accept.

        """"""
        >>> shell.ast_transformers
        [...]
        
        """

        if not any(x for x in shell.ast_transformers if isinstance(x, ReturnYield)):
            shell.ast_transformers.append(ReturnYield())



    class PidginTransformer(IPython.core.inputtransformer2.TransformerManager):
        def pidgin_transform(self, cell: str) -> str: 
            tokens = self.tokenizer.parse(''.join(cell))
            return self.tokenizer.untokenize(tokens)
        
        def pidgin_cleanup(self, cell: str) -> list: 
            return self.pidgin_transform(cell).splitlines(True)
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.tokenizer = Tokenizer()
            self.cleanup_transforms.insert(0, self.pidgin_cleanup)
            self.line_transforms.append(demojize)

        def pidgin_magic(self, *text): 
            """Expand the text to tokens to tokens and 
            compact as a formatted `"python"` code."""
            return IPython.display.Code(self.pidgin_transform(''.join(text)), language='python')
        



    import ast
    class ReturnYield(ast.NodeTransformer):
        def visit_FunctionDef(self, node): return node
        visit_AsyncFunctionDef = visit_FunctionDef
        def visit_Return(self, node):
            replace = ast.parse('''__import__('IPython').display.display()''').body[0]
            replace.value.args = node.value.elts if isinstance(node.value, ast.Tuple) else [node.value]
            return ast.copy_location(replace, node)

        def visit_Expr(self, node):
            if isinstance(node.value, (ast.Yield, ast.YieldFrom)):  return ast.copy_location(self.visit_Return(node.value), node)
            return node
        
        visit_Expression = visit_Expr



    import mistune as markdown, textwrap, __main__, IPython, typing, re, IPython, nbconvert, ipykernel, doctest, ast
    __all__ = 'pidgin',



    class Tokenizer(markdown.BlockLexer):
            """
### Tokenizer

<details>
<summary>Tokenize `input` text into `"code" and not "code"` tokens that will be translated into valid `python` source.</summary>
        
            """
            class grammar_class(markdown.BlockGrammar):
                doctest = doctest.DocTestParser._EXAMPLE_RE

            def parse(self, text: str, default_rules=None) -> typing.List[dict]:
                if not self.depth: self.tokens = []
                with self: tokens = super().parse(whiten(text), default_rules)
                if not self.depth: tokens = self.compact(text, tokens)
                return tokens

            def parse_doctest(self, m): self.tokens.append({'type': 'paragraph', 'text': m.group(0)})

            def parse_fences(self, m):
                if m.group(2): self.tokens.append({'type': 'paragraph', 'text': m.group(0)})
                else: super().parse_fences(m)

            def parse_hrule(self, m):
                self.tokens.append({'type': 'hrule', 'text': m.group(0)})

            def compact(self, text, tokens):
                """Combine non-code tokens into contiguous blocks."""
                compacted = []
                while tokens:
                    token = tokens.pop(0)
                    if 'text' not in token: continue
                    else: 
                        if not token['text'].strip(): continue
                        block, body = token['text'].splitlines(), ""
                    while block:
                        line = block.pop(0)
                        if line:
                            before, line, text = text.partition(line)
                            body += before + line
                    if token['type']=='code':
                        compacted.append({'type': 'code', 'lang': None, 'text': body})
                    else:
                        if compacted and compacted[-1]['type'] == 'paragraph':
                            compacted[-1]['text'] += body
                        else: compacted.append({'type': 'paragraph', 'text': body})
                if compacted and compacted[-1]['type'] == 'paragraph':
                    compacted[-1]['text'] += text
                elif text.strip():
                    compacted.append({'type': 'paragraph', 'text': text})
                return compacted

            depth = 0
            def __enter__(self): self.depth += 1
            def __exit__(self, *e): self.depth -= 1

            def untokenize(self, tokens: τ.List[dict], source: str = """""", last: int =0) -> str:
                INDENT = indent = base_indent(tokens) or 4
                for i, token in enumerate(tokens):
                    object = token['text']
                    if token and token['type'] == 'code':
                        if object.lstrip().startswith(FENCE):

                            object = ''.join(''.join(object.partition(FENCE)[::2]).rpartition(FENCE)[::2])
                            indent = INDENT + num_first_indent(object)
                            object = textwrap.indent(object, INDENT*SPACE)

                        if object.lstrip().startswith(MAGIC):  ...
                        else: indent = num_last_indent(object)
                    elif not object: ...
                    else:
                        object = textwrap.indent(object, indent*SPACE)
                        for next in tokens[i+1:]:
                            if next['type'] == 'code':
                                next = num_first_indent(next['text'])
                                break
                        else: next = indent       
                        Δ = max(next-indent, 0)

                        if not Δ and source.rstrip().rstrip(CONTINUATION).endswith(COLON): 
                            Δ += 4

                        spaces = num_whitespace(object)
                        "what if the spaces are ling enough"
                        object = object[:spaces] + Δ*SPACE+ object[spaces:]
                        if not source.rstrip().rstrip(CONTINUATION).endswith(QUOTES): 
                            object = quote(object)
                    source += object

                for token in reversed(tokens):
                    if token['text'].strip():
                        if token['type'] != 'code': 
                            source = source.rstrip() + SEMI
                        break

                return source 
            
    for x in "default_rules footnote_rules list_rules".split():
        setattr(Tokenizer, x, list(getattr(Tokenizer, x)))
        getattr(Tokenizer, x).insert(getattr(Tokenizer, x).index('block_code'), 'doctest')
        
    ...
    """
</details>&nbsp;

    """
    pidgin = PidginTransformer()


A potential outcome of a `pidgin` program is reusable code. 

Import pidgin notebooks as modules.


    class PidginLoader(__import__('importnb').Notebook): 
        extensions = ".ipynb .md.ipynb".split()
        def code(self, str): return ''.join(pidgin.transform_cell(str))



    class PidginPreprocessor(nbconvert.preprocessors.Preprocessor):
        def preprocess_cell(self, cell, resources, index, ):
            if cell['cell_type'] == 'code':
                cell['source'] = pidgin_transformer.transform_cell(''.join(cell['source']))
            return cell, resources


The shell is the application either jupyterlab or jupyter notebook, the kernel determines the programming language.  Below we design a just jupyter kernel that can be installed using 

    !pidgin kernel install


    class PidginInteractiveShell(IPython.InteractiveShell):
        """Configure a native `pidgin` `IPython.InteractiveShell`"""
    PidginInteractiveShell.input_transformer_manager.default_value = PidginTransformer
    PidginInteractiveShell.enable_html_pager.default_value = True

    class PidginKernelApp(ipykernel.kernelapp.IPKernelApp): 
        """Configure a native `pidgin` `__import__('ipykernel').kernelapp.IPKernelApp"""
    PidginKernelApp.shell.default_value = PidginInteractiveShell



    graphviz.Source(
digraph{rankdir=UD 
subgraph cluster_pidgin {label="new school" PIDGIN->{PYTHON MARKDOWN}}
subgraph cluster_web {label="old school" WEB->{PASCAL TEX} }}
    
    )



## testing `"code"` in the `markdown` narrative.
[📔](testing.md.ipynb)

In literate programs, `"code"` is deeply entangled with the narrative.
`"code"` object can signify meaning and can be validated through testing.
`python` introduced the `doctest` literate programming convention that indicates some text in a narrative can be tested.
`pidgin` extends the `doctest` opinion to the inline markdown code.
Each time a `pidgin` cell is executed, the `doctest`s and inline code are executed ensuring that
any code in a `pidgin` program is valid.



    def post_run_cell(result):
        result.runner = test_markdown_string(result.info.raw_cell, IPython.get_ipython(), False, doctest.ELLIPSIS)

    def load_ipython_extension(shell): 
        unload_ipython_extension(shell)
        shell.events.register('post_run_cell', post_run_cell)



    import doctest, contextlib, mistune as markdown, re, ast, __main__, IPython, operator
    shell = IPython.get_ipython()


`test_markdown_string` extends the standard python `doctest` tools 
to inline code objects written in markdown.  
This approach compliments are markdown forward programming language to test
intertextual references between code and narrative.


    INLINE = re.compile(
        markdown.InlineGrammar.code
        .pattern[1:]
        .replace('[\s\S]*', '?P<source>[\s\S]+')
        .replace('+)\s*', '{1,2})(?P<indent>\s{0})'), 
    )


    (TICK,), SPACE = '`'.split(), ' '



    def test_markdown_string(str, shell=shell, verbose=False, compileflags=None):
        globs, filename = shell.user_ns, F"In[{shell.last_execution_result.execution_count}]"
        runner = doctest.DocTestRunner(verbose=verbose, optionflags=compileflags)  
        parsers = DocTestParser(runner), InlineDoctestParser(runner)
        parsers = {
            parser: doctest.DocTestFinder(verbose, parser).find(str, filename) for parser in parsers
        }
        examples = sum([test.examples for x in parsers.values() for test in x], [])
        examples.sort(key=operator.attrgetter('lineno'))
        with ipython_compiler(shell):
            for example in examples:
                for parser, value in parsers.items():
                    for value in value:
                        if example in value.examples:
                            with parser:
                                runner.run(doctest.DocTest(
                                    [example], globs, value.name, filename, example.lineno, value.docstring
                                ), compileflags=compileflags, clear_globs=False)
        shell.log.info(F"In[{shell.last_execution_result.execution_count}]: {runner.summarize()}")
        return runner



    @contextlib.contextmanager
    def ipython_compiler(shell):
        def compiler(input, filename, symbol, *args, **kwargs):
            nonlocal shell
            return shell.compile(
                ast.Interactive(
                    body=shell.transform_ast(
                        shell.compile.ast_parse(input)
                    ).body
                ),
                F"In[{shell.last_execution_result.execution_count}]",
                "single",
            )

        yield setattr(doctest, "compile", compiler)
        try:
            doctest.compile = compile
        except:
            ...





## Weaving the `markdown` to a rich display.
[📗](exports.md.ipynb)

This is the weaving step.



    import datetime, dataclasses, sys, IPython as python, IPython, nbconvert as export, collections, IPython as python, mistune as markdown, hashlib
    exporter, shell = export.exporters.TemplateExporter(), python.get_ipython()
    modules = lambda:[x for x in sys.modules if '.' not in x and not str.startswith(x,'_')]



Markdown input can fail to render when jinja2 is used in correctly.  Markdown is never wrong, but sometimes jinja is.



    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-1-25dc2f3cd961> in <module>
    ----> 1 @dataclasses.dataclass
          2 class Metadata:
          3     def pre_run_cell(self, info):
          4         self.modules = modules()
          5         self.start = datetime.datetime.utcnow().isoformat()


    NameError: name 'dataclasses' is not defined





    ---------------------------------------------------------------------------

    UndefinedError                            Traceback (most recent call last)

    ~/anaconda3/lib/python3.7/site-packages/jinja2/asyncsupport.py in render(self, *args, **kwargs)
         74     def render(self, *args, **kwargs):
         75         if not self.environment.is_async:
    ---> 76             return original_render(self, *args, **kwargs)
         77         loop = asyncio.get_event_loop()
         78         return loop.run_until_complete(self.render_async(*args, **kwargs))


    ~/anaconda3/lib/python3.7/site-packages/jinja2/environment.py in render(self, *args, **kwargs)
       1006         except Exception:
       1007             exc_info = sys.exc_info()
    -> 1008         return self.environment.handle_exception(exc_info, True)
       1009 
       1010     def render_async(self, *args, **kwargs):


    ~/anaconda3/lib/python3.7/site-packages/jinja2/environment.py in handle_exception(self, exc_info, rendered, source_hint)
        778             self.exception_handler(traceback)
        779         exc_type, exc_value, tb = traceback.standard_exc_info
    --> 780         reraise(exc_type, exc_value, tb)
        781 
        782     def join_path(self, template, parent):


    ~/anaconda3/lib/python3.7/site-packages/jinja2/_compat.py in reraise(tp, value, tb)
         35     def reraise(tp, value, tb=None):
         36         if value.__traceback__ is not tb:
    ---> 37             raise value.with_traceback(tb)
         38         raise value
         39 


    <template> in top-level template code()


    ~/anaconda3/lib/python3.7/site-packages/jinja2/environment.py in getattr(self, obj, attribute)
        432             pass
        433         try:
    --> 434             return obj[attribute]
        435         except (TypeError, LookupError, AttributeError):
        436             return self.undefined(obj=obj, name=attribute)


    UndefinedError: 'syntax' is undefined



## `pidgin` metasyntax at language interfaces.
[📗]({{pathlib.Path(syntax.__file__).name}})

The combinations of document, programming, and templating languages
provides unique syntaxes as the interfaces.

{{appendix.exports(syntax)}}



### Reusing `pidgin` documents.

Notebooks gain value when they be reusable at rest.

We'll make a cli application that deploys `pidgin` as a web, cli, converter.


    @click.group()
    def pidgin(): 
The `pidgin` command line application operates on passive notebooks
documents.



    @pidgin.command()
    def serve(modules):
Serve notebook modules from fastapi creating an openapi schema for each 
literate document.



    @pidgin.command()
    def run(modules, parallel=True):
Run a collection of notebook modules.



    @pidgin.command()
    def convert(modules):
Convert notebook written in pidgin to difference formats.


