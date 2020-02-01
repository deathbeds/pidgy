[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/deathbeds/pidgin/again)


`pidgin` is a literate programming designed specifically for `jupyter` `notebook`s running `IPython` kernels.
It is an `IPython` extension that can be loaded with

<code>%load_ext pidgin</code>

If you need to install `pidgin`, you can install it from `"pypi"`

<code>pip install pidgin</code> 



`pidgin` provides a `markdown and python` literate programming interface for `jupyter` `notebook`.
Authors will develop documentation and source code at the same time,
wherein literary excellence is the goal.
When a cell is executed in `pidgin` mode:
1. The fenced & indented code in `markdown` is executed as python.
2. Any `doctest`s and inline code are unit tested.
3. The `markdown` `input` is passed into a `template` engine then rendered by `jupyter`'s rich display system.

