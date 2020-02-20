# Literature as the test

    import pidgy, pytest, nbval, doctest, importnb.utils.pytest_importnb
    if __name__ == '__main__':
        import notebook, IPython as python

Intertextuallity emerges when the primary target of a program is literature.
Some of the literary content may include `"code"` `object`s that can be tested
to qualify the veracity of these dual signifiers.

`pidgy` documents are designed to be tested under multiple formal testing
conditions. This is motivated by the `python`ic concept of documentation
testing, or `doctest`ing, which in itself is a literate programming style. A
`pidgy` document includes `doctest`, it verifies `notebook` `input`/`"output"`,
and any formally defined tests are collected.

    class pidgyModule(importnb.utils.pytest_importnb.NotebookModule):

`pidgy` provides a `pytest` plugin that works only on `".md.ipynb"` files. The
`pidgy.kernel` works directly with `nbval`, install the python packkage and use
the --nbval flag. `pidgy` uses features from `importnb` to support standard
tests discovery, and `doctest` discovery across all strings. Still working on
coverage. The `pidgyModule` permits standard test discovery in notebooks.
Functions beginning with `"test_"` indicate test functions.

        loader = pidgy.pidgyLoader

    class pidgyTests(importnb.utils.pytest_importnb.NotebookTests):

if `pidgy` is install then importnb is.

        modules = pidgyModule,
