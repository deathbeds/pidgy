# Introduction

A contemporary challenge for science is reprogramming literature for an information-rich scientific economy. Recently, science is troubled with an inability to reproduce scientific results from their published methods. This reproducibility crisis highlights the inability of natural language to bring meaning to data. In response, open science communities demonstrate that programming languages can supplement natural language as they are better equipped to communicate meaning in data. These progressive workflows disrupt traditional scientific publications with hypertext and hypermedia that are unbound from the constraints of physical media. These changes mean that modern scientific communications will necessitate different literacies when computability becomes a formal feature of scientific literature.

“Notebooks” have been adopted by differently-abled scientists and authors across disciplines to share stories supplemented with data and code. The availability of millions of open source notebooks demonstrates the potential of interleaved narrative, code, and hypermedia in computational thinking. The Jupyter Notebook ecosystem allows once-isolated scientific experiences to be shared in reproducible units through polyglot scientific languages. While the peer review process still requires a human reviewer to measure literary value, computational veracity can be automatically measured when an author adopts software engineering best practices.

![](literate_computing_venn.jpeg)

Literate programming is a prescient, multi-lingual style of documentation that approaches programs as literary works. Minimally, a literate program is constrained to a document format and a programming language. Respectively, Donald Knuth’s WEB implementation chose TeX and Pascal, while Jupyter notebooks use a pidgin of Markdown, TeX mathematical notation, tables, and syntax highlighting, and accept over 100 different programming languages. In a 2013 essay, Fernando Perez, author of IPython, describes literate computing as weaving interactive computation into scientific narratives, a different concern than the literary and computational qualities of the literate program. A strict separation of these concerns creates inconsistencies, both for the author and reader, between the document and the program.

`pidgy` bridges literate programming and computing interactive programming experience that assigns Markdown as the primary programming language. The literate computing read-eval-print-loop allows composing documentation and software concurenntly. `pidgy` modifies the customizable `IPython` shell and kernel to:

1. before execution, tangle code line-for-line from Markdown to valid IPython syntax.
2. after execution, the input is woven into different representations:

   1. the outcome of formal `unittest and doctest`.
   2. template the Markdown using `jinja2` syntax and show a rich [Markdown] display.

Documents are composed interactively, and the introduction of literate program conventions for the REPL helps the ensure literary and computational integrity throughout the document. The `pidgy` is implemented as a literate program such that the `pidgy` paper and module are derived from the same sources, similarly, `pidgy` source code is used on the formal testing. `pidgy` demonstrates the flexability of literate code on different continuous integration systems for testing on Github Actions, publishing on Read the Docs, and packaging Pypi.

![](pidgy_literate_computing.jpeg)

["literate computing" and computational reproducibility]: http://blog.fperez.org/2013/04/literate-computing-and-computational.html
[tools for the life cycle of a computational idea]: https://sinews.siam.org/Details-Page/jupyter-tools-for-the-life-cycle-of-a-computational-idea
[tex]: #
[web]: #
[pascal]: #
[markdown]: #
[fernando perez]: #
[literate computing]: #
[notebooks]: #
[literate programming]: #
[`ipython`]: #
[literate program]: #
[documentation]: #
[tangle]: #
[weave]: #
