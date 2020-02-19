# Building the `pidgy` extension

    def load_ipython_extension(shell):
The `pidgy` implementation uses the `IPython` configuration
and extension system to modify the interactive computing expierence
in `jupyter` notebooks.
        
        translate.load_ipython_extension(shell)
1. The primary function of `pidgy` is that it imports `markdown` as formal language for 
programming multiobjective literate programs.  imports focuses on the indentification of
`"code" and not"code"` that become python code.

        testing.load_ipython_extension(shell) 
2. The `pidgy` specification promotes strong intertextuality between `"code" and not"code"` 
objects in a program.  `testing` reinforces that efficacy of the `"code"` using
documentation tests of `doctest and "inline"+"code"`.  `pidgy` uses the narrative a formal 
test for the program.  These tests are executed interactively to ensure the veracity of 
`"code"` signs in the narrative.

        reuse.load_ipython_extension(shell)
        outputs.load_ipython_extension(shell)
3. Literate computing in `pidgy` allows incremental development of `"code"` and the co-development of the documentation.
`pidgy` interprets the `input` `"code"` as a `display`.  `pidgy` uses a `template` language to transclude
`object`s from code 

    
    def unload_ipython_extension(shell):
        for x in (outputs, testing, translate): 
            x.unload_ipython_extension(shell)

    
    import jupyter, notebook, IPython, mistune as markdown, IPython as python, ast, jinja2 as template, importnb as _import_, doctest, pathlib
    with _import_.Notebook(lazy=True): 
        try: from . import reuse, translate
        except: import reuse, translate
    with reuse.pidgyLoader(lazy=True): 
        try: 
            from . import outputs
            from .tests import interactive as  testing
        except: 
            import outputs
            from tests import interactive as testing