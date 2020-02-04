# `pidgy` programming



`🐦,pidgy` programming is a fun and expressive style of literate computing
designed for writing nonfiction literate in `jupyter` computational `📓`s.
It presents a `M⬇️`-forward style of programming where authors
codevelop code and narrative. 
`pidgy`programs are intermediate documents 
that can be read, written, and formally tested.



pidgy programming is a style of literate computing,
it is an expressive way of writing program


pidgy programming is concerned with scientific literacy, the general abilities to read & write scientific literature, and the implicit pleasure of interactively
composing modern literate programs.
Access to commodity computing infrastructures have affected 
the forms of scientific information architecture and 
scientific literature.
Programming languages represent novel forms
that express heuristics that are explicitly reusable, they fill the voids where 
the superior code of language fails to communicate phenomenon.
Scientific literature written in `pidgy` accept all 
languages equitably, it assigns language the role of communicating
computational thought in fluid combinations of human or machine logic.




# Literary code & coded literature



    """
literate `pidgy` programs have two intents:
1. be literature that acts as a program.
2. be a program that acts as literature.

In this approach, programming languages merge with natural language
to communicate thought.  As a whole, these documents encapsulate
unstructured languages that communicate with combinations of human 
and machine logic.  

    """;



    class pidgyLoader(__import__('importnb').Notebook): 
        """
The `pidgyLoader` includes `pidgy` documents in Python's import system.
        
        """
        extensions = ".md.ipynb".split()
        """
Regardless of intent, `pidgy` programs should be reusable in other programs.
`pidgy` programs are identified by the composite file extension `".md.ipynb"`.
The choice is file extension is made because `pidgy` programs 
designed primarly for literate programming in `jupyter` `notebook`s - 
that use the `".ipynb"` suffix - 
with `markdown` as the document language and `IPython` as the glue programming language.
        
        """
        def code(self, str): 
            """
Appply the pidgy transformers.
        
            """
            return ''.join(__import__('pidgy').translate.pidgy.transform_cell(str))



## Authoring reusable documents.



    """
For documents to be reused as modules, they must restart and run all.

A benefit of this approach is that the documents can be tested.

    """;





# Deriving files from `pidgy` documents.



There are numerous tools that use the `notebook` format as an intermediate formats
for different documents.

The original literate programming used latex as the sole export format
where as the notebook recognizes quite a few formats:
    
<details><summary><code>nbconvert</code> can generate <b>12</b> different formats from the files that abide the <code>nbformat</code>
schema.</summary>
<ul><li>html</li>
<li>python</li>
<li>asciidoc</li>
<li>notebook</li>
<li>slides</li>
<li>pdf</li>
<li>latex</li>
<li>selectLanguage</li>
<li>custom</li>
<li>script</li>
<li>markdown</li>
<li>rst</li>
</ul>
</details>




    class pidgyTranslate(nbconvert.preprocessors.Preprocessor):
        def preprocess_cell(self, cell, resources, index, ):
            import pidgy
            if cell['cell_type'] == 'code':
                cell['source'] = pidgy.imports.pidgy.transform_cell(''.join(cell['source']))
            return cell, resources



    class pidgyNormalize(nbconvert.preprocessors.Preprocessor):
Untangle a pidgy notebook into a normalized notebook that explicitly sepearting code and markdown cells.
A normalized notebook can be imported by importnb.
        
        def preprocess(self, nb, resources):
            new, tokens = nbformat.v4.new_notebook(), []
            for cell in nb.cells:
                for token in tokenizer.parse(''.join(cell.source)) if cell.cell_type == 'code' else [{'type': 'paragraph', 'text': ''.join(cell.source)}]:
                    new.cells.append((
                        nbformat.v4.new_code_cell if token['type'] == 'code' else nbformat.v4.new_markdown_cell
                    )(token['text'].splitlines(True)))
            return nb, resources





## Literature as the test

Literate `pidgy` programs accomodate varities of syntaxes and opinions.
`pidgy` takes the opinion that everything that is code is computable.
Interactive doctests are tested.



`pidgy` provides a `pytest` plugin that works only on `".md.ipynb"` files.
The `pidgy.kernel` works directly with `nbval`, install the python packkage and use the --nbval flag.
`pidgy` uses features from `importnb` to support standard tests discovery, 
and `doctest` discovery across all strings.

Still working on coverage.



    class pidgyModule(importnb.utils.pytest_importnb.NotebookModule):
The `pidgyModule` permits standard test discovery in notebooks.
Functions beginning with `"test_"` indicate test functions.

        loader = pidgy.imports.pidgyLoader



    class pidgyTests(importnb.utils.pytest_importnb.NotebookTests):
        modules = pidgyModule,

    pytest_collect_file = pidgyTests.__call__





# Building the `pidgy` extension


    def load_ipython_extension(shell):
The `pidgy` implementation uses the `IPython` configuration
and extension system to modify the interactive computing expierence
in `jupyter` notebooks.
        
        imports.load_ipython_extension(shell)
1. The primary function of `pidgy` is that it `imports` `markdown` as formal language for 
programming multiobjective literate programs.  `imports` focuses on the indentification of
`"code" and not"code"` that become python code.

        testing.load_ipython_extension(shell) 
2. The `pidgy` specification promotes strong intertextuality between `"code" and not"code"` 
objects in a program.  `testing` reinforces that efficacy of the `"code"` using
documentation tests of `doctest and "inline"+"code"`.  `pidgy` uses the narrative a formal 
test for the program.  These tests are executed interactively to ensure the veracity of 
`"code"` signs in the narrative.

        exports.load_ipython_extension(shell)
3. Literate computing in `pidgy` allows incremental development of `"code"` and the co-development of the documentation.
`pidgy` interprets the `input` `"code"` as a `display`.  `pidgy` uses a `template` language to transclude
`object`s from code 







![svg](paper.md_files/paper.md_6_0.svg)




## programming in `markdown and python` 
[📓](translate.ipynb)


    def load_ipython_extension(shell):
        """
The `pidgy` `load_ipython_extension`'s primary function transforms the `jupyter`
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
        pidgy_transformer = pidgyTransformer()        
        shell.input_transformer_manager = pidgy_transformer
        
        """
`IPython` provides configurable interactive `shell` properties.  Some of the configurable properties
control how `input` code is translated into valid source code. 
The `pidgy` translation is managed by a custom `IPython.core.inputtransformer2.TransformerManager`.
        
        """"""
        >>> shell.input_transformer_manager
        <...pidgyTransformer object...>
        
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



    class pidgyTransformer(IPython.core.inputtransformer2.TransformerManager):
        def pidgy_transform(self, cell: str) -> str: 
            tokens = self.tokenizer.parse(''.join(cell))
            return self.tokenizer.untokenize(tokens)
        
        def pidgy_cleanup(self, cell: str) -> list: 
            return self.pidgy_transform(cell).splitlines(True)
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.tokenizer = Tokenizer()
            self.cleanup_transforms.insert(0, self.pidgy_cleanup)
            self.line_transforms.append(demojize)

        def pidgy_magic(self, *text): 
            """Expand the text to tokens to tokens and 
            compact as a formatted `"python"` code."""
            return IPython.display.Code(self.pidgy_transform(''.join(text)), language='python')
        



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
    __all__ = 'pidgy',



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
    pidgy = pidgyTransformer()


A potential outcome of a `pidgy` program is reusable code. 

Import pidgy notebooks as modules.


    class pidgyLoader(__import__('importnb').Notebook): 
        extensions = ".ipynb .md.ipynb".split()
        def code(self, str): return ''.join(pidgy.transform_cell(str))



    class pidgyPreprocessor(nbconvert.preprocessors.Preprocessor):
        def preprocess_cell(self, cell, resources, index, ):
            if cell['cell_type'] == 'code':
                cell['source'] = pidgy_transformer.transform_cell(''.join(cell['source']))
            return cell, resources



    graphviz.Source(
digraph{rankdir=UD 
subgraph cluster_pidgy {label="new school" pidgy->{PYTHON MARKDOWN}}
subgraph cluster_web {label="old school" WEB->{PASCAL TEX} }}
    
    )



## testing `"code"` in the `markdown` narrative.
[📔](interactive.md.ipynb)

In literate programs, `"code"` is deeply entangled with the narrative.
`"code"` object can signify meaning and can be validated through testing.
`python` introduced the `doctest` literate programming convention that indicates some text in a narrative can be tested.
`pidgy` extends the `doctest` opinion to the inline markdown code.
Each time a `pidgy` cell is executed, the `doctest`s and inline code are executed ensuring that
any code in a `pidgy` program is valid.



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
[📗](outputs.md.ipynb)





## `pidgy` metasyntax at language interfaces.
[📗](test_pidgin_syntax.md.ipynb)

The combinations of document, programming, and templating languages
provides unique syntaxes as the interfaces.

This is a code string




`pidgy` programming is a `markdown`-forward approach to programming,
it extends computational to interactive literate programming environment.
One feature `markdown` uses to identify `markdown.BlockGrammar.block_code`
is indented code.
`pidgy` starts here, all cells are `markdown` forward, and code is identified as indented code.

            "This is a code string"
    



### Code fences

Some folks may prefer code fences and they may be used without a language specified.


```
"This is code"
```

```python
"This is not code."
```



    class DocStrings:
### Docstrings


    >>> assert DocStrings.__doc__.startswith('### Docstrings')
    >>> DocStrings.function_docstring.__doc__
    '`DocStrings.function_docstring`s appear as native docstrings, ...'


        def function_docstring():
`DocStrings.function_docstring`s appear as native docstrings, but render as `markdown`.
            
            ...

    





    import doctest
### `doctest`

    >>> assert True
    >>> print
    <built-in function print>
    >>> pidgy
    <module...__init__.py'>



### templating

filters
jinja docs





### Reusing `pidgy` documents.

Notebooks gain value when they be reusable at rest.

We'll make a cli application that deploys `pidgy` as a web, cli, converter.

# `pidgy` command line application



    import click, IPython, pidgy



    @click.group()
    def app(): 
The `pidgy` command line application operates on passive notebooks
documents.



    @app.group()
    def kernel():
Serve notebook modules from fastapi creating an openapi schema for each 
literate document.

    @kernel.command()
    def install(user=False, replace=None, prefix=None):
        with pidgy.translate.pidgyLoader():
            from .kernel import shell
        dest =shell.install(user=user, replace=replace, prefix=prefix)
        click.echo(F"The pidgy kernel was install in {dest}")
        
    @kernel.command()
    def uninstall(user=True, replace=None, prefix=None):
        with pidgy.translate.pidgyLoader():
            from .kernel import shell
        shell.uninstall()
        click.echo(F"The pidgy kernel was removed.")
        



    @app.command()
    def serve(modules):
Serve notebook modules from fastapi creating an openapi schema for each 
literate document.



    @app.command()
    def run(modules, parallel=True):
Run a collection of notebook modules.



    @app.command()
    def convert(modules):
Convert notebook written in pidgy to difference formats.



