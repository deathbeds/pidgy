#!/usr/bin/env -S python -m midgy 
# `pidgy`'s tangle and weave implementations


`pidgy` is a literate computing implementation that turns converts markdown into valid python. when working in `pidgy`, we simultaneously develop narrative and code together. `pidgy` brings new affordances to communicating computational narratives in markdown scripts and jupyter notebooks

## literate programming conventions

[donald knuth] authored the original paper on literate programming. in this work, he outlines an approach to programming that treats programs as essays wherein the author strives for literary excellence. this prescient, seminal work is a delightful paper that expresses the joy and pleasure we can acheive when writing good programs.

from a technical position, knuth - the patron saint of yakshaves - defines two key units of work when operating on literate programs:

1. the tangle step refers to translating a document language to a programming language
2. the weave step that formats and displays that document

### tangle and weave language choices

the reference `web` implementation of literate programming chose:

1. tex as a document language
2. pascal as a scripting language

`midgy` is an ~~post~~modern take that chooses markdown and python, respectively.

### markdown as a document language

markdown is chosen because of its wide spread adoption across the programming universe. it is a permissive language that never breaks, it only fails expectations. it can encapsulate any progamming language including itself.

commonmark
markdown-it-py is commonmark

### python as a scripting language

python is an idiomatic programming language that, at times, can read _near_ to natural language. we can look back to the early roots of python and its goal of computing for everyone. python is now the most popular programming language, and markdown is the gateway to programming.

cp4e 

### `tangle.py` - `pidgy` tangle

while designing `pidgy`, we chose the following constraints:

* line for line
* valid python
* no interactive comptue specific heuristics
* document language can't fail

`pidgy` uses `tangle.py` to codify the heuristics for translating markdown to python. it provides an extensible class that can be extending using the underlying `markdown-it-py` machinery.

in `tangle.py`, significant work happens in the `Tangle.Python.code_block` and `Tangle.Python.noncode_block` methods. these methods do the work of translating markdown elements to python.

### `weave.py` - `pidgy` weave

`midgy` can be used as:

* a command line interface to execute markdown files and `midgy` notebooks
* an ipython extension that modifies your interactive computing interface

in each of these applications we target different markdown representations of the document. the cli provides an `ansi` markdown view, and the interactive computing application renders `html`. in both outcomes, the same markdown source can be used.

`weave.py` defines several flags to be implemented to improve the literate computing experience.

#### literate computing influences and impacts

`midgy`'s design and implementation is informed by work in jupyter notebooks and the need to write better stories with code. literate computing is an extension of literate programming that weaves live computation in the narrative.

##### `midgy` notebooks

##### explicit versus implicit displays

## `midgy` metalanguage

the markdown trigger for code in literate programs are code fences. the fence markers `\`\`\`` from a strict delination between code and noncode. further, these implementations extend programmatic control using the optional fence information. these affordances ensure that narrative will not naturally flow into code.

`midgy` focuses purely on white space, which is complementary to the underlying python language. indented code, or white space aware code, reduces the separation between narrative and code. in the end, they even cooperate.

### define variables of markdown strings

        a_variable_of_markdown =\
this string is assigned to `a_variable_of_markdown`.

        a_variable_with_lotsa_continuation =\
        \
        \
python's line continuation syntax extends naturally to `midgy`. it is the primary interface for connecting markdown and python with `midgy`.

### explicit quotes

when `midgy` encounters python block quotes `"\""` or `'''` the author controls body


        a_stripped_tight_string = """
> this will still display as markdown and the `str.strip` method is applied at the end.

        """.strip()

we can even include docstring

### markdown docstrings

another encouraging impact of `midgy` are markdown docstrings.

        def my_function_with_a_docstring():
the markdown block immediately following function definitions becomes the function docstring. this happens because `midgy` indents markdown blocks immediately following a `:`.


        class MyClassWithADocstrings:
the same heuristics apply nicely for class definitions.

                ... # sometimes we need provide null code to control indenting


### parenthetic `midgy` syntax

`midgy` 

#### the captured docstrings

```text
# proof that we know the docstring
## my_function_with_a_docstring
{{my_function_with_a_docstring.__doc__}}

## MyClassWithADocstrings
{{MyClassWithADocstrings.__doc__}}
```

## conflicting opinions

* magic functions - specific to ipython not python
* truncating markdown blocks with null operators `...`, `pass`, `""`, `# comment`
* hiding output during the weave step
* line continuations

## examples

* this document
* dev.md
* gist
* dataframes

## measurable outcomes

* we can reproduce acheive dvi document formats with the python ecosystem
* its fun to write programs in this style
* runnable documents/shebang

## conclusion

`midgy` is really powerful for small ideas, it is provides natural affordances for combining code and narrative into executable stories

[literate programming]: #
[donald knuth]: #
[literate computing]: #
[cp4e]: #
[indented code blocks]: https://spec.commonmark.org/0.30/#indented-code-blocks
[fenced code blocks]: https://spec.commonmark.org/0.30/#fenced-code-blocks