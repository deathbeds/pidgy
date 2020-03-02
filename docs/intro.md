---
tangle_weave_diagram: https://user-images.githubusercontent.com/4236275/75093868-bdb12e80-557d-11ea-8989-efd6a733a8e0.png
---

# Introduction to literate programs and computable essays.

> I believe that the time is ripe for significantly better documentation of
> programs, and that we can best achieve this by considering programs to be
> works of literature.
>
> > [Donald Knuth]

<!--The introduction should be written as a stand alone essay.-->
<!--

    try: from . import figures
    except: ...

-->

"[Literate programming]" is a pioneering paper published by [Donald Knuth] in 1979. It
describes a multiobjective, multilingual style of programming that treats programs
primarily as documentation. Literate programs have measures along two dimensions:

1. the literary qualities determined the document formatting language.
2. the computational qualities determined by the programming language.

The multilingual nature of literate program creates the opportunity
for programmers and non-programmers to contribute to the same literature.

Literate programs accept `"code"` as an integral part of the narrative.
`"code"` signs can be used in places where language lacks just as figures and equations are used in scientific literature.
An advantage of `"code"` is that it can provide augmented representations
of documents and their symbols that are tactile and interactive.

![Tangle Weave Diagram]({{tangle_weave_diagram}})

The literate program concurrently describes a program and literature.
Within the document, natural language and the programming language interact
through two different process:

1. the tangle process that converts to the programming language.
2. the weave process that converts to the document formatting language.

The original WEB literate programming implementation chose to tangle to Pascal and weave to Tex. `pidgy`'s modern take on literate programming tangles to [Python] and weaves to [Markdown], and they can be written in either [Markdown] files or `jupyter` `notebooks`.

[Pascal] was originally chosen for its widespread use throughout education,
and the same can be said for the choice of `jupyter` `notebook`s used
for education in many programming languages, but most commonly [Python].
The preferred document language for the `notebook` is [Markdown]
considering it is part of the notebook schema.
CP4E
The motivations made the natural choice for a [Markdown] and [Python]
programming lanuage.
Some advantages of this hybrid are that Python is idiomatic and
sometimes the narrative may be explicitly executable.

[Literate Programming] is alive in places like [Org mode for Emacs], [RMarkdown], [Pweave], [Doctest], or [Literate Coffeescript].
A conventional look at literate programming will place a focus on the final document. `pidgy` meanwhile places a focus on the interactive literate computing steps required achieve a quality document.

Originally, `pidgy` was designed specifically for the `notebook` file format, but it failed a constraint
of not being an existing file.
Now `pidgy` is native for [Markdown] files, and valid testing units.
It turns out the [Markdown] documents can provide
a most compact representation of literate program,
relative to a notebook. And it diffs better.

Design constraints:

- Use an existing file formats.
- Minimal bespoke syntax.
- Importable and testable

A last take on this work is to affirm the reproducibly of enthusiasm when writing literate programs.

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
