# `pidgy` literate computing toolkit

`pidgy` is a extension of `IPython` that allows for literate programming in notebooks and markdown files.


## `pidgy` features

### programming python in markdown

the primary work of `pidgy` is define heuristics that translate markdown into valid python code. `pidgy` attaches special rules that interleave blocks of markdown into python code; for example, in `pidgy` docstrings look just like normal markdown.

#### lisp flavored literate programming in python

python is a whitespace aware language, and requires special rules for rendering python code. `pidgy` provides `hy` a python flavored lisp that allows for another mode literate programming.

### writing scripts in markdown files

by translating markdown to python, `pidgy` can use markdown as a literate scripting language where markdown files operate as if they were python modules

### interactive notebook displays

`pidgy` supports `jinja2` templates out of the box, and can embed rich display objects created by `IPython`.

### formal testing interfaces

`pidgy` brings support for `unittest` and `doctest`. testing fixtures are executed with each cell executed.

### em😄ji suport

`pidgy` supports emojis through their aliases or explicit emoji.