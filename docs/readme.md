<style>
.jp-mod-presentationMode {
    --jp-notebook-padding: 0;
}
.jp-RenderedHTMLCommon pre code {
    opacity: 0.25;
}
.jp-Placeholder-content .jp-MoreHorizIcon {
    background-size: 32px;
}
</style><style>
.jp-mod-presentationMode .jp-SideBar,
.jp-mod-presentationMode #jp-top-panel {
    opacity: 0.0;
    transition: all 0.2s;
}
.jp-mod-presentationMode .jp-SideBar:hover,
.jp-mod-presentationMode #jp-top-panel:hover {
    opacity: 0.9;
    transition: all 0.2s;
}</style><style>
.jp-mod-presentationMode.jp-ApplicationShell,
.jp-mod-presentationMode .p-TabBar-content{
    background-color: var(--jp-layout-color0);
}
</style><style>
.jp-mod-presentationMode .p-DockPanel-widget,
.jp-mod-presentationMode #jp-left-stack{
    border-color: transparent;
}
.jp-mod-presentationMode .jp-Toolbar-item,
.jp-mod-presentationMode .jp-Toolbar {
    opacity: 0.1;
    transition: all 0.2s;
}
.jp-mod-presentationMode .jp-Toolbar-item:hover,
.jp-mod-presentationMode .jp-Toolbar:hover {
    opacity: 0.9;
    transition: all 0.2s;
}

.jp-mod-presentationMode .jp-InputArea {
    flex-direction: column;
}

</style><style>
.jp-mod-presentationMode .jp-Notebook .jp-Cell .jp-InputPrompt, 
.jp-mod-presentationMode .jp-Notebook .jp-Cell .jp-OutputPrompt {
    flex: 0 0 2rem !important;
    opacity: 0;
}
.jp-mod-presentationMode .jp-Notebook .jp-Cell.jp-mod-active .jp-OutputPrompt,
.jp-mod-presentationMode .jp-Notebook .jp-Cell.jp-mod-active .jp-OutputPrompt {
    opacity: 0.5;
}
.jp-mod-presentationMode .jp-Notebook .jp-Cell .jp-InputPrompt, 
.jp-mod-presentationMode .jp-Notebook .jp-Cell .jp-OutputPrompt

.jp-mod-presentationMode hr {
    opacity: 0.1;
}
</style>
    <style>
    .jp-TableOfContents-content h1, 
    .jp-TableOfContents-content h2 {
        margin-bottom: var(--jp-ui-font-size0);
    }
    </style>

    <style>
    .jp-mod-presentationMode {
        --jp-content-heading-line-height: 1.25 !important;
    }
    </style>

    <style>
    .jp-mod-presentationMode #jp-main-status-bar {
        opacity: 0.06;
        transition: all 0.2s;
    }
    .jp-mod-presentationMode #jp-main-status-bar:hover {
        opacity: 0.8;
        transition: all 0.2s;
    }
    </style>




# `pidgy` programming



`🐦,pidgy` programming is a fun and expressive style of literate computing
designed for writing nonfiction literature in `jupyter` computational `📓`s.
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



    with importnb.Notebook():
        try: from . import translate
        except: import translate



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
            return ''.join(translate.pidgy.transform_cell(str))



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

A strong intertextuallity may emerge when 
the primary target of a document is literature.
Some of the literary content may include `"code"` `object`s
that can be tested to qualify the veracity of these
dual signifiers.

`pidgy` documents are designed to be tested under
multiple formal testing conditions.
This is motivated by the `python`ic concept of documentation testing,
or `doctest`ing, which in itself is a literate programming style.
A `pidgy` document includes `doctest`, it verifies `notebook` `input`/`"output"`,
and any formally defined tests are collected.



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





![svg](output_1_0.svg)




# `pidgy` co-developments

`pidgy` documents are written in `markdown`,
and `"code"` is an intertextual feature of the narrative.
We'll find that `pidgy` documents can serve many purposes like:
* being a piece of literature.
* being a piece of documentation.
* being a testing unit.
* being a `python` module.
* being a command line application.
* being a web service.

`markdown`as a programming language can encapsulate
any formal programming languages as
either block or fenced objects.
They are literate programs that combine human & machine logic 
to provide enriched meaning to the document.



`pidgy`'s literate programs are designed to be reused in multiple contexts.



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





# The `pidgy` shell-kernel model


The shell is the application either jupyterlab or jupyter notebook, the kernel determines the programming language.  Below we design a just jupyter kernel that can be installed using 

    !pidgy kernel install


    def install(kernel_name='pidgy',
        user=True,
        replace=None,
        prefix=None
    ):
        return ipykernel.kernelspec.KernelSpecManager().install_kernel_spec(
            str(pathlib.Path(globals().get('__file__', pathlib.Path('spec'))).parent/'spec'), kernel_name=kernel_name,
            user=user, replace=replace, prefix=prefix)



    def uninstall(kernel_name='pidgy',):
        ipykernel.kernelspec.KernelSpecManager().remove_kernel_spec(kernel_name)





# Building the `pidgy` extension






![svg](paper.md_files/paper.md_8_0.svg)




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


    UndefinedError: 'translate' is undefined



## programming in `markdown and python` 
[📓]({{pathlib.Path(translate.__file__).name}})


{{appendix.exports(pidgy.translate)}}

    graphviz.Source(
digraph{rankdir=UD 
subgraph cluster_pidgy {label="new school" pidgy->{PYTHON MARKDOWN}}
subgraph cluster_web {label="old school" WEB->{PASCAL TEX} }}
    
    )



## testing `"code"` in the `markdown` narrative.
[📔](interactive.md.ipynb)

    import IPython as python, doctest, textwrap
    pidgy= None



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



    import doctest



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
                        shell.compile.ast_parse(shell.transform_cell(textwrap.indent(input, ' '*4)))
                    ).body
                ),
                F"In[{shell.last_execution_result.execution_count}]",
                "single",
            )

        yield setattr(doctest, "compile", compiler)
        doctest.compile = compile





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



