# The `pidgy` package and paper

`pidgy` is a fun way to interactively program in [Markdown]. It is design
to tell stories with data and code in your favorite IDE ([jupyter], [nteract], [colab], [vscode]).
 and use them in python modules, scripts, and applications.

 It that allows fluid combinations of code and prose with added language features like block markdown variables, emoji variables names, and interactive formal testing. It is designed primarily for Jupyter notebooks and Markdown source files.


[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/deathbeds/pidgy/master?urlpath=lab)
[![Documentation Status](https://readthedocs.org/projects/pidgy/badge/?version=latest)](https://pidgin-notebook.readthedocs.io/en/latest/?badge=latest)
![Python package](https://github.com/deathbeds/pidgy/workflows/Python%20package/badge.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pidgy)

```bash
pip install pidgy    # Install pidgy
```

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

    def task_sphinx():
build the pidgy docs with sphinx and is configured by conf.py
    
        return dict(actions="sphinx-build . docs".splitlines())
    
    def task_book():
build the pidgy docs with jupyter book. 
    
        return dict(actions="jupyter-book build .".splitlines())
    
    def task_docs_config():
build the pidgy docs with jupyter book. 
    
        return dict(actions="jupyter-book config sphinx . > conf.py".splitlines())

    def task_test():
test the pidgy package.
    
        return dict(actions=[
            doit.tools.Interactive("pytest --nbval --sanitize-with sanitize.cfg -p no:warnings pidgy/tests/test_* docs/examples")
            ])


    def task_build():
build the pidgy package
    
        return dict(actions="".splitlines())        


[markdown]: https://en.wikipedia.org/wiki/Markdown
[python]: https://python.org
[jupyter]: https://jupyter.org
[nteract]: https://nteract.io
[colab]: #
[vscode]: #