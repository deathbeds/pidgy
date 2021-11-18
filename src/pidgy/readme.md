#!/usr/bin/env -S python -m pidgy 
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

`pidgy` is an ~~post~~modern take that chooses markdown and python, respectively.

### markdown as a document language

markdown is chosen because of its wide spread adoption across the programming universe. it is a permissive language that never breaks, it only fails expectations. it can encapsulate any progamming language including itself.

commonmark
markdown-it-py is commonmark

### python as a scripting language

python is an idiomatic programming language that, at times, can read _near_ to natural language. we can look back to the early roots of python and its goal of computing for everyone. python is now the most popular programming language, and markdown is the gateway to programming.

cp4e 


[literate programming]: #
[donald knuth]: #
[literate computing]: #
[cp4e]: #
[indented code blocks]: https://spec.commonmark.org/0.30/#indented-code-blocks
[fenced code blocks]: https://spec.commonmark.org/0.30/#fenced-code-blocks