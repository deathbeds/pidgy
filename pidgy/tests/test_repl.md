# Stepping along `IPython`'s [Read-Eval-Print-Loop]

> Sometimes I think the only universal in the computing field is the fetch-execute cycle.
>
> > _Alan Perlis - Perlisisms_

The [Read-Eval-Print-Loop], a fetch-execute cycle, is a familiar interface to execute code and
programs run by a compiler. The `IPython` project orginally began as an
terminal application that was designed to improve the interactive experience
when working [Python]. Eventually, `IPython` moved outside the terminal and
into the browser with `IPython` notebooks that allowed authors that capture
the process of their computational thinking supplemented with supporting
hypermedia.

    import pytest
    @pytest.mark.skipif(not __import__('IPython').get_ipython(), "There is no IPython.")
    def test_ipython_repl():

The body `IPython_REPL` demonstrates that components of the interactive shell that may be configured.

shell = IPython.get_ipython()

### Read

`IPython` triggers events when the REPL begins.

        shell.events.callbacks.get('pre_execute'), shell.events.callbacks.get('pre_run_cell')

Once the `input` is read, `IPython` applies a series of strings transformations when the cell is transformed.
The outcome of the transformation should be some that [Python] can `compile`.

        shell.transform_cell, [
            shell.input_transformer_manager.cleanup_transforms,
            shell.input_transformer_manager.line_transforms,
            shell.input_transformer_manager.token_transformers
        ]

The [Python] code is translated into an [Abstract Syntax Tree].

        shell.compile.ast_parse

Transformations to AST are applied by a series of transformers.

        shell.transform_ast, shell.ast_transformers

### Eval

    The `shell` run the body of the [Abstract Syntax Tree] and

        shell.run_ast_nodes, (

### Print

formats any node meeting the criteria for the ast node interactivity. Typically, the last expression is shown.

        ),shell.ast_node_interactivity,shell.display_formatter.format...

`IPython` triggers events when the REPL ends.

        shell.events.callbacks.get('post_run_cell'), shell.events.callbacks.get('post_execute')

### Loop
