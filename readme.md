# `pidgy` minimal literate computing

`pidgy` is a [literate computing] tool that translates markdown into executable python. it presents a new style of programming, in the `pidgy` metalanguage, that treat literature written in markdown as python programs.

this project features some serious things and some fun things:

- a python package for literate progamming with documentation and tests

  ```
    pip install pidgy
  ```

- a command line application for executing markdown files

  ```
    pidgy filename.md
  ```

- interactive computing tools for jupyter notebooks

  ```
    %load_ext pidgy
  ```

- a jupyter kernel

  ```
    python -m pidgy.kernel.install
  ```

- a complete research paper describing the project and history

  published on the [readthedocs] with jupyter book.

  ```
    nox -s docs # build the docs locally
  ```

- a lot of care

a goal with `pidgy`, and its derivatives, is to have fun writing and reading programs. to evoke joy in the author(s) and transmit their spirit. we'll begin by writing the programs we wish we'd read.

[literate computing]: docs/literate-programming.html#literate-computing
[readthedocs]: https://pidgy.readthedocs.io/
