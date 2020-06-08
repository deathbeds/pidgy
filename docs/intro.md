# Introduction

`pidgy` is hyperliterate programming that emerges from the union of literate programming and literate computing. In ["Literate computing" and computational reproducibility"], Fernando Perez, creator of IPython, distinguishes literate computing as the process of weaving live computation into a narrative, . The outcome of the act of interactive literate computing is a document that is a literate program. Literate programs are an extension pre-digital literature that rely on the intertextuality of text and code to communicate meaning. Together, literate programming and computing represent an evolution to hyperliterature that includes hypertext and hypermedia to bring meaning.

Pidgin programming invokes as many languages as necessary to bring meaning to a concept.  Recently, science is troubled with an inability to reproduce scientific results from their published methods. This reproducibility crisis highlights the inability of natural language to bring meaning to data. In response, open science communities demonstrate that programming languages can supplement natural language as they are better equipped to communicate meaning in data. These progressive workflows disrupt traditional scientific publications with hypertext and hypermedia that are unbound from the constraints of physical media. These changes mean that modern scientific communications will necessitate different literacies when computability becomes a formal feature of scientific literature.

The influence of literate computing means that computational notebooks, speficallyJupyter ne IPython notebooks, are a key technology for `pidgy`. A conventional notebooks will separate units of text into different cells. Narrative cells are written in Markdown, and code cells are written in >100 languages. The distinct separation of cells limits the interplay text and code in a literate program. `pidgy` proposes a full Markdown forward approach to writing code, narrative and code cells are both Markdown. In a code cell, Markdown is translated/tangled into the target kernel language and executed. The result is a document that permissively allows the interplay of hypertext and hypermedia within a document of heterogenous media.

“Notebooks” have been adopted by differently-abled scientists and authors across disciplines to share stories supplemented with data and code. The availability of millions of open source notebooks demonstrates the potential of interleaved narrative, code, and hypermedia in computational thinking. The Jupyter Notebook ecosystem allows once-isolated scientific experiences to be shared in reproducible units through polyglot scientific languages. While the peer review process still requires a human reviewer to measure literary value, computational veracity can be automatically measured when an author adopts software engineering best practices.

`pidgy` bridges literate programming and computing interactive programming experience that assigns Markdown as the primary programming language. The literate computing read-eval-print-loop allows composing documentation and software concurenntly. `pidgy` modifies the customizable `IPython` shell and kernel to:

1. before execution, tangle code line-for-line from Markdown to valid IPython syntax.
2. after execution, the input is woven into different representations:

   1. the outcome of formal `unittest and doctest`.
   2. template the Markdown using `jinja2` syntax and show a rich [Markdown] display.

Documents are composed interactively, and the introduction of literate program conventions for the REPL helps the ensure literary and computational integrity throughout the document. The `pidgy` is implemented as a literate program such that the `pidgy` paper and module are derived from the same sources, similarly, `pidgy` source code is used on the formal testing. `pidgy` demonstrates the flexability of literate code on different continuous integration systems for testing on Github Actions, publishing on Read the Docs, and packaging Pypi.



![](literate_computing_venn.jpeg)


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
