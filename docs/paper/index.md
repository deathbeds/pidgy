# `pidgy` programming

## Abstract

`pidgy` is a literate program that specifies and implements a literate
programming language using [Markdown] as the document formatting language and
[Python] as the programming language. The implementation extends the interactive
python shell that commonly powers `jupyter` notebooks. Through this program we
will learn how `pidgy` tangles markdown to python code, incrementally runs
formal tests on your input, and presents woven markdown output that allows for
transclusion of variables.

## Topics

- Literate Programming
- Computational Notebooks
- Markdown
- Python
- Jupyter
- IPython

## Author

[Tony Fast]

<!--

    import __init__ as paper
    import nbconvert, pathlib, click
    file = pathlib.Path(locals().get('__file__', 'readme.md')).parent / 'index.ipynb'


    @click.command()
    def build():
        file.with_suffix('.md').write_text(
            nbconvert.get_exporter('markdown')(
                exclude_input=True).from_filename(
                    str(file))[0])
        click.echo(F'Built {file.with_suffix(".md")}')

    if __name__ == '__main__':
         build() if '__file__' in locals() else build.callback()


-->

[tony fast]: #
[markdown]: #
[python]: #
[jupyter]: #
[ipython]: #

## Introduction

What problems did literate programming solve:

- Literacy and readability take precedence over coding excellence.
- Non-programmers can contribute.

> ” I am imposing a moral commitment on everyone who hears the term; surely
> nobody wants to admit writing an illiterate program.

> I believe that the time is ripe for significantly better documentation of
> programs, and that we can best achieve this by considering programs to be
> works of literature.

> In fact, my enthusiasm is so great that I must warn the reader to discount
> much of what I shall say as the ravings of a fanatic who thinks he has just
> seen a great light.

What problems am I solving.

- A markdown python literate program hybrid. python is an idiomatic programming
  language with the intent of being a computer programming (language) for
  everyone.
- Interleaving markdown and code narrative.
- A more diff friendly literate programming source code.
- Add interactivity to the literate programming process.

<!--The introduction should be written as a stand alone essay.-->

"[Literate programming]" is a paper published by [Donald Knuth] in 1979. It
describes a style of programming that promotes a literary approach to writing
programs as documentation. Literate programs are measured along two dimensions:
literary and computational quality.

[Literate Programming] is alive in places like [Org mode for Emacs],
[RMarkdown], [Jupyter Notebooks], [Doctest], or [Literate Coffeescript].

`pidgy` imagines an adoption of [Literate Programming] as documentation for
data-driven computational narratives.  
`pidgy` implements a literate computing interface for `jupyter` using open
source scientific computing infrastructure.

The outcome of writing `pidgy` programs are readable, reusable, and reproducible
documents.  
`pidgy` natively supports importing markdown and notebooks as source code.

Modern computing has different pieces of software infrastructure than were
available

[literate programming]: #
[donald knuth]: #
[literate coffeescript]: #
[org mode for emacs]: #
[jupyter notebooks]: #
[rmarkdown]: #
[doctest]: #

## The interactive `pidgy` interface

`pidgy` documents are written in interactive programming environments that make
it easy to run code and preview outputs. This specific implementation is bound
to the `IPython` kernel to be used in `jupyter` `notebook` and `jupyterlab`.

<!--

    import jupyter, notebook, IPython, mistune as markdown, IPython as python, ast, jinja2 as template, importnb as _import_, doctest, pathlib
    with _import_.Notebook(lazy=True):
        try: from . import reuse, translate
        except: import reuse, translate
    with reuse.pidgyLoader(lazy=True):
        try: from . import outputs, testing
        except: import outputs, testing
-->

    def load_ipython_extension(shell: IPython.InteractiveShell) -> None:

The `load_ipython_extension and unload_ipython_extension` are functions that can
configure the `IPython.InteractiveShell`. We'll introduce a few major features
that are configured everytime `pidgy` is used interactively.

1.  Configure the ability to import other `pidgy` markdown files and notebooks
    as python modules.  
    reuse.load_ipython_extension(shell)

2.  Perhaps the most labourious part of `pidgy` are the heuristics for a
    line-by-line translation of markdown source to python.

            translate.load_ipython_extension(shell)

3)  `pidgy` documents will frequently sprinkle `"code"` throughout a document.
    It uses this code as interactive test objects that are run as unit tests.

            testing.load_ipython_extension(shell)

4.  The `pidgy` `input` represents both code and design. We trigger a few custom
    output events to capture reproducible information about the computing
    environment.  
    outputs.load_ipython_extension(shell)

<!--

    def unload_ipython_extension(shell):
        for x in (outputs, testing, translate):
            x.unload_ipython_extension(shell)

-->

<!--


```python

    __all__ = 'pidgyLoader',
    import pidgy, sys, IPython, mistune as markdown, importnb, IPython as python
    if __name__ == '__main__':
        shell = get_ipython()
```

-->

## Reusable computable literature

A primary requirement is that `pidgy` documents can be included in other `pidgy`
documents, and, consequently, other `python` tools. To acheive this, `pidgy`
modifies how `python` finds `__import__`s, this is acheived with an existing
tool called `importnb` that includes `notebook` documents in `sys.path_hooks`
used to discover modules.

```python
    def load_ipython_extension(shell):
        pidgyLoader(position=-1, lazy=True).__enter__()
```

A successful implementation will make it possible to include markdown and
notebooks as having the same equity as python source code in a literate
programming project. The notebook allows extra information to be stored. To
identify `pidgy` `notebook`s against other notebooks we introduce the hybrid
extension `".md.ipynb"`.

```python
    class pidgyLoader(importnb.Notebook):
        extensions = ".md .md.ipynb".split()


        def code(self, str):
            """
The `"code"` method of the `__import__` loader
performs string transforms to code cells.
`pidgy` uses the same method
that the `shell.input_transformer_manager`.


            """
            with importnb.Notebook(lazy=True):
                try: from . import translate
                except: import translate
            return ''.join(translate.pidgy.transform_cell(str))

        def visit(self, node):
            """
The `"visit"` method provides modifications to the
abstract syntax tree.

            """
            with importnb.Notebook():
                try: from . import translate
                except: import translate
            return translate.ReturnYield().visit(node)

        def get_data(self, path):
            if self.path.endswith('.md'):
                return self.code(self.decode())
            return super().get_data(path)

        get_source = get_data

```

```python

    def unload_ipython_extension(shell): ...
```
