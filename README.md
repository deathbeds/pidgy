# `pidgy` hyperactive programmings

`pidgy` is a fun way to interactively program in [Markdown] and [IPython]. It is design
to tell stories with code, tests, and data in your favorite IDE ([jupyter], [nteract], [colab], [vscode]).
 It that allows fluid combinations of code and prose with added language features like block markdown variables, emoji variables names, and interactive formal testing. It is designed primarily for Jupyter notebooks and Markdown source files that can be used as python modules, scripts, and applications.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/deathbeds/pidgy/master?urlpath=lab)
[![Documentation Status](https://readthedocs.org/projects/pidgy/badge/?version=latest)](https://pidgin-notebook.readthedocs.io/en/latest/?badge=latest)
![Python package](https://github.com/deathbeds/pidgy/workflows/Python%20package/badge.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pidgy)

```bash
pip install pidgy    # Install pidgy
```

## `pidgy` features

* interleave narrative and code in the same cells
* test literate notebooks and programs
* transclude real data into narratives with `jinja2` templates
* reactive displays that update on rendering

## the pidgy shell/kernel

`pidgy` is installed as `jupyter` kernel that can be used in lab or classic.
`pidgy` opens authors into a markdown forward programming interface.

* the kernel can be installed manually using the cli.

```bash
pidgy kernel install # install the pidgy kernel.
```

## authoring `pidgy` documents

in `pidgy`, code is indented. both markdown and python cells accept markdown in `pidgy`. as a result, in `pidgy` markdown cells are consider off and code are considered on. the indented code pattern is valid in standard `IPython` kernels and pidgy.

## Importing `pidgy` documents

`pidgy` extends the python import system to include `".ipynb"` and `".md"` files along with native `".py"` files.

    with __import__("pidgy").pidgyLoader(): 
        import README

## The `pidgy` CLI

The `pidgy` cli helps to tangle and weave entire literate pidgy programs.

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

## developer

`pidgy` uses `doit` to make tests and documentation work.

    import doit.tools

### tasks


    def task_book():
`pidgy` builds document with the `jupyter_book` project. 

        return dict(actions="jupyter-book build .".splitlines())

    def task_sphinx():

the `"conf.py"` for sphinx in generated from the `jupyter_book` cli.

        return dict(actions="sphinx-build . docs".splitlines())

    def task_test():
`pidgy` tests notebooks using plugins from `importnb` and [`nbval`]
    
        return dict(actions=[
            doit.tools.Interactive("pytest --nbval --sanitize-with sanitize.cfg -p no:warnings pidgy/tests/test_* docs/examples")
        ])


[markdown]: https://en.wikipedia.org/wiki/Markdown
[python]: https://python.org
[jupyter]: https://jupyter.org
[nteract]: https://nteract.io
[colab]: #
[vscode]: #
[`importnb`]: https://github.com/deathbeds/importnb
[`nbval`]: https://github.com/computationalmodelling/nbval/