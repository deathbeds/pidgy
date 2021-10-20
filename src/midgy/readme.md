# about the project

`midgy` is the most minimal implementation of a white space aware literate programming language with python as a base scripting language. `midgy` identifies indented blocks as executable code, and everything else is considered markdown strings. through this approach we develop a metalanguage that allows markdown and python to cooperate.

## literate programming conventions

donald knuth defined to aspects of literate programming:

1. the tangle step refers to translating a document language to a programming language
2. the weave step that formats and displays that document

### `tangle.py`

`tangle.py` codifies the heuristics for translating markdown to python. it provides an extensible class that can be extending using the underlying `markdown-it-py` machinery.

### `weave.py`

`midgy` can be used as:

* a command line interface to execute markdown files and `midgy` notebooks
* an ipython extension that modifies your interactive computing interface

in each of these applications we target different markdown representations of the document. the cli provides an `ansi` markdown view, and the interactive computing application renders `html`. in both outcomes, the same markdown source can be used.

## `midgy` metalanguage

the markdown trigger for code in literate programs are code fences. the fence markers `\`\`\`` from a strict delination between code and noncode. further, these implementations extend programmatic control using the optional fence information. these affordances ensure that narrative will not naturally flow into code.

`midgy` focuses purely on white space, which is complementary to the underlying python language. indented code, or white space aware code, reduces the separation between narrative and code. in the end, they even cooperate.

### markdown docstrings

an encouraging impact of `midgy` are markdown docstrings.

        def my_function_with_a_docstring():
the markdown block immediately following function definitions becomes the function docstring. this happens because `midgy` indents markdown blocks immediately following a `:`.


        class MyClassWithADocstrings:
the same heuristics apply nicely for class definitions.

                ... # sometimes we need provide null code to control indenting


### transclusion/templating

`midgy` 

#### the captured docstrings

```text
# proof that we know the docstring
## my_function_with_a_docstring
{{my_function_with_a_docstring.__doc__}}

## MyClassWithADocstrings
{{MyClassWithADocstrings.__doc__}}
```
