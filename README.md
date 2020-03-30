# The `pidgy` package and paper

`pidgy` is a fun way to program in [Markdown] in your favorite IDE (jupyter, nteract, colab, vscode) that can be reused as python modules, scripts, and applications.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/deathbeds/pidgy/master?urlpath=lab)
[![Documentation Status](https://readthedocs.org/projects/pidgy/badge/?version=latest)](https://pidgin-notebook.readthedocs.io/en/latest/?badge=latest)
![Python package](https://github.com/deathbeds/pidgy/workflows/Python%20package/badge.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pidgy)

```bash
pip install pidgy    # Install pidgy
```

`pidgy` has a few components to it:

- It is an interactive [Literate Computing] implementation of `IPython`
- A specification of a _potentially_ polyglot approach for literate programming applied to other languages.
- A complete unit of computable scientific literate. It is written in a literate programming style with the literature as the primary outcome. _Read the `pidgy` paper_.

## The pidgy shell and kernel

`pidgy` can be used as a native `jupyter` kernel in Jupyter, nteract, colab, and vscode. Install the kernel with

```bash
pidgy kernel install # install the pidgy kernel.
```

Or, in your standard Python shell, load the `pidgy` `IPython` extension.

## Importing `pidgy` documents

`pidgy` uses the `importnb` machinery to import files into [Python] that are not native `".py"` files.

    import pidgy
    with pidgy.pidgyLoader(): ...

## The `pidgy` CLI

```text
Usage: pidgy [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  kernel
  render
  run       `pidgy` `run` makes it possible to execute `pidgy` documents as...
  template
  test      Formally test markdown documents, notebooks, and python files.
  to
```
