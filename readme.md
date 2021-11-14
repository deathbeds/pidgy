# `pidgy` minimal literate computing

`pidgy` is formal [literate computing] library that translates markdown into executable python. it presents a new style of programming, in the `pidgy` metalanguage, that brings new affords markdown files and notebooks.

this project features some serious things and some fun things:

* a python package for literate progamming with documentation and tests

        pip install pidgy

* a command line application for executing markdown files

        pidgy filename.md

* interactive computing tools for jupyter notebooks

        %load_ext pidgy

* a jupyter kernel

        python -m pidgy.kernel.install

* a complete research paper describing the project and history

        nox -s docs

* a lot of care

a goal with `pidgy`, and its derivatives, is to have fun writing and reading programs. to evoke joy in the author(s) and transmit their spirit. we'll begin by writing the programs we wish we'd read.
