# `pidgy` minimal literate computing

`pidgy` is a Markdown-forward flavor of Python; it thinks of Markdown as code and transpiles, line-for-line to Python.[^line4line] It is a literate programming implementation designed for a tighter weave of narrative and code.

`pidgy` can combines several popular parsing conventions to provide an enhanced authoring experience for Python programs. The `pidgy` flavor allows authors to consider the following concepts in a single document:

* Computation and execution with Python
* Documentation and rendering with Markdown
* Templating with `jinja2`
* Testing with `doctest and unittest`
* Interaction with Jupyter Notebooks and IPython as Jupyter kernel

## Usage

this project features some serious things and some fun things:

* A python package for literate progamming with documentation and tests

        pip install pidgy

* A command line application for executing markdown files

        pidgy filename.md

* Interactive computing tools for jupyter notebooks

        %load_ext pidgy

* A Jupyter kernel

        python -m pidgy.kernel.install

A goal with `pidgy`, and its derivatives, is to have fun writing and reading programs. to evoke joy in the author(s) and transmit their spirit. we'll begin by writing the programs we wish we'd read.

## The `pidgy` conventions

Literate programming defines two layers of processing:

1. The `tangle` phase that transpiles the document language (Markdown) to programming language (Python)
2. The `weave` phase that transforms the document language (Mardown) to the rendered view.

### tangle `pidgy`

In literate programming, the transpilation of the document to code is called the tangle step. When `pidgy` translates Markdown to Python:

* Indented code is translated one-for-one, line-for-line to Python; code fences are treated as block string NOT Python.
* All other Markdown blocks are treated as block strings dedented relative to the indented code. This allows Markdown blocks to be used in Python statements and expressions including docstrings.
* Is aware of `doctest` statements and separa.

### weave `pidgy`

When we weave a document, we want to see something like HTML or PDF. When we weave `pidgy`:

* Markdown acts as our primary rendering interface for plain-text or HTML.
* `jinja2` allows Python variables to be included in the rendered document.
* `doctest and unittest` provide visual feedback on any test cases in the narrative.

## Why `pidgy`?

`pidgy` is designed to build new ideas through story-telling. Our most nascent ideas require us to bring code to language. In `pidgy`, we treat code (and tests) as literary devices.

Markdown and Python are natural candidates for a literate programming language. Markdown as document language is beginner friendly; it doesn't fail, but violates expectation. Learning Markdown is practical modern communcation skill given the mass adoption across applications. Python as a programming language is designed to be an idiomatic language that natural to speak.

With `pidgy` we want to explore the intersections of the natural literary affordances both Markdown and Python provide. 

### Literate Computing

`pidgy`s inspiration come from interactive computing in Jupyter notebooks. Notebooks are a natural literate programming interface, but the create a stark boundary between code and narrative. `pidgy` sought to resolve this separation and explore a tighter integration between the two. `pidgy` testing and templating integrations are a product of this path.

`pidgy` programs can be executed & rendered based on the state of the variables. `jinja2` templates allow `pidgy` authors to include and manipulate Python variables when the document is woven then rendered. 

Jupyter Notebooks have always been a go to tool for testing ideas. `pidgy` formalizes this concept by elevating `doctest` blocks as a primary language feature. With aware of `doctest`s, and `unittest`s in an interactive context, we can weave tests results into interactive & static narratives.


[literate computing]: docs/literate-programming.html#literate-computing
[readthedocs]: https://pidgy.readthedocs.io/
