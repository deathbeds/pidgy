    import IPython, pidgy

    @IPython.core.magic_arguments.magic_arguments()
    @IPython.core.magic_arguments.argument('--ipython', action='store_false', help='Apply IPython transforms.')
    @IPython.core.magic_arguments.argument('--tokens', action='store_true', help='Show tokens.')
    def tangle(line, cell):
        import IPython
        args = IPython.core.magic_arguments.parse_argstring(tangle, line)
        if cell:
            if args.tokens:
                out = IPython.display.JSON(pidgy.tangle.Tangle().parse(cell), expanded=True)
            else:
                out = IPython.display.Code((pidgy.tangle.pidgyManager().transform_cell if args.ipython else pidgy.tangle.tangle)(cell), language='python')
            IPython.display.display(out)

    def render(line, cell):

Render a template with the variables in the current namespace.

        if cell:
            IPython.display.display(IPython.display.Markdown(pidgy.weave.Weave(IPython.get_ipython()).render(cell)))

    def load_ipython_extension(shell):
        shell.register_magic_function(tangle, 'line_cell')
        shell.register_magic_function(render, 'line_cell')

    def unload_ipython_extension(shell): ...
