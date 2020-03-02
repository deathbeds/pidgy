# Literature as the test

    import pidgy, pytest, nbval, doctest, importnb.utils.pytest_importnb

Literate documents can be motivated by the need to test a concept. In a fact, a common
use case of notebooks is that they interactively test units of thought. Often the thought
of reusability is an after thought.

`pidgy` documents are meant to be treated as test objects. In fact, the `pidgy` test suite
executed by `pytest` through [Github Actions][actions] uses `pidgy` notebooks (ie. documents with the `".md" or ".md.ipynb"` extension). `pidgy` supplies its own `pytest` extensions, and it uses [`nbval`][nbval] and the `pytest`"--doctest-modules"`flag. With these conditions we discover pytest conventions, unitests, doctests, and options cell input output validated. Ultimately,`pidgy` documents may represent units of literate that double as formal test objects.

The document accessed by the `"pytest11"` console_script and includes the extension with a pytest runner.

    class pidgyModule(importnb.utils.pytest_importnb.NotebookModule):

The `pidgyModule` derives from an existing `pytest` extension that extracts formal tests from `notebook`s
as if they were regular python files. We'll use the `pidgy.pidgyLoader` to load Markdown-forward documents
as python objects.

        loader = pidgy.pidgyLoader

    class pidgyTests(importnb.utils.pytest_importnb.NotebookTests):

`pidgyTests` makes sure to include the alternative source formats to tangle to python executions.

        modules = pidgyModule,

[nbval]: https://github.com/computationalmodelling/nbval/ "The pidgy kernel works directly with `nbval`."
[actions]: https://github.com/deathbeds/pidgy/runs/478462971
