# Introduction

A contemporary challenge for science is reprogramming literature for an information rich scientific economy. Recently, science is troubled with an inability to reproduce scientific results from their methods. This reproducibility crisis highlights the lacking ability of language to bring meaning to data. In response, open science communities demonstrate that programming languages can supplement the lack of natural language as they are better equipped to communicate meaning in data. These progressive workflows disrupt traditional scientific publications with hypertext and hypermedia that are unbound from the constraints of physical media. Modern scientific communications necessitate different approach literacies when programming languages become formal features in scientific literature.

Recently, polyglot Jupyter notebooks have been adopted by differently abled scientists and authors across disciplines to share stories supplemented with data and code. The availability of millions of notebooks demonstrates the need to interleave narrative, code, and hypermedia in computational thinking. The Jupyter Notebook ecosystem allows isolated scientific experiences to be shared in reproducible units through polyglot scientific languages. The peer review process still requires a reviewer to measure literary value, but the computational veracity can be measured by adopting best practices in open source software engineering.

Literate programming is a prescient multi-lingual style of computing that approaches programs as literary works. Minimally, literate programs define document formatting and programming languages. Respectively, Donald Knuth’s WEB implementation chose Tex and Pascal, while Jupyter notebooks use Markdown formatting and accept over 100 different programming languages. In a 2013 essay, Fernando Perez, author of IPython, describes literate computing as weaving interactive computation into scientific narratives, which is a different concern than the literary and computational qualities of the literate program. A strict separation of these concerns creates inconsistencies between the documentation and program.

`pidgy` implements an interactive programming experience that unites literate computing and programming by making Markdown the primary programming language. It modifies the popular IPython kernel and interactive shell to accept Markdown, and when executed is tangled to Python then woven as a rich display.

![](literate_computing_venn.jpeg)

![](pidgy_literate_computing.jpeg)

Throughout this work we'll design a purpose built interactive literate computing interface. This work is interested in designing an interactive experience that results in multi-objective computational documents that are readable, reusable, and reproducible over longer timelines than single use notebooks and programs.
A consistent theme is that all interactions were designed for `jupyter`, and as a result end-user of `jupyter` kernels like colab and vscode can use `pidgy`.
The intent of `pidgy` matured as different features began to take form. Originally, `pidgy` was gungho about [Notebooks] being the primary interface for Literate Programming. [Notebooks] provide a metastable serialization of the Literate Programming containing both the literate input and the woven hypermedia. And they still serve valid applications for conditions where the input and output are highly dependent on each other. There are other conditions where we desire to write programmatic literature that is reliably reproducible over a longer timeline. [Markdown] written in `pidgy` seems to provide a compact input for pythonic literate programs with [Markdown] first. If a program is reproducible, then it is input of its outputs.

![](degrees_of_freedom.jpg)

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
