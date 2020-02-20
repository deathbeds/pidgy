# `pidgy` literate `notebook` programming

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/deathbeds/pidgy/master?urlpath=lab)
[![Documentation Status](https://readthedocs.org/projects/pidgin-notebook/badge/?version=latest)](https://pidgin-notebook.readthedocs.io/en/latest/?badge=latest)
![Python package](https://github.com/deathbeds/pidgy/workflows/Python%20package/badge.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pidgy)

`pidgy` combines ideas from literate programming and modern software practices
to introduce markdown-forward python syntax.  
The result is are programs that focus equally literary and computational
quality, what results are documents with rich intertextuality between natural
language and programming languages.

`pidgy` is an extension for the interactive python - `IPython` - shell and an
`IPython` kernel.  
It can be used when editting markdown documents and `jupyter` notebooks in
`jupyterlab`. When `pidgy` is enabled:

- Write code in `markdown`, indented and fenced are executed.
- `doctest`s in `markdown` are tested.
- Include `object`s in `markdown` with `jinja2` `template` syntax.
- `notebook`s can be woven and tangled as documentation and code.
- `notebook`s can be reproduced as tests.
- `".md.ipynb"` is a composite extension that indicates `pidgy` `notebook`s
  primarly written in `markdown`

## The `pidgy` programming paper.

`pidgy` is a literate program, meaning it is written narrative first with a
secondary capability of being a reusable program.

    import pidgy

## `pidgy` command line application

### Install the `IPython` kernels

Install the `pidgy` kernel so you can use whenever you want.

```bash
pidgy kernel install
```

### Load the `IPython` extension

Otherwise, using the `pidgy` `IPython` extension any `jupyter` `notebook`.

```bash
%load_ext pidgy
```

Likely, the only other paper of the api you made need is the `pidgy.pidgyLoader`
that allows `pidgy` documents to be imported as normal source code. The loader
searches for `notebook`s with the `".md.ipynb"` extension and adds them to the
python import system.

## reuse `pidgy` documents as modules

    with pidgy.pidgyLoader():
        import readme
    assert readme.__file__.endswith('.md.ipynb')

## testing `pidgy` notebooks.

`pidgy` is a `pytest` plugin that can be used to include literature (eg. blog
posts, issues, docs) in software test suites.

```bash
pytest --nbval--doctest-modules readme.md.ipynb
```

## The plurality of `pidgy`

Above we've highlight a few outcomes of `pidgy` programming. `pidgy` is written
as both documentation and source code therefore it can be viewed by the
following tools.

- [nbviewer](https://nbviewer.jupyter.org/github/deathbeds/pidgy/blob/master/readme.md.ipynb)
- [github pages](https://deathbeds.github.io/pidgy/)
- [pypi](https://pypi.org/project/pidgy)
- [readthedocs](https://pidgin-notebook.readthedocs.io/en/latest/)
- [binder](https://mybinder.org/v2/gh/deathbeds/pidgy/master)
- [github actions](https://github.com/deathbeds/pidgy/actions)
