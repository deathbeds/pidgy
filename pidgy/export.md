Literate programs can be translated into many formats. Commonly markup langauges focus on translation to other markup languages, we add an extra ability to convert markup to source code.

    import pidgy, pathlib

    def to_markup(input, exporter):
        return exporter.from_notebook_node(nbformat.v4.new_notebook(cells=[nbformat.v4.new_markdown_cell(input)]))[0]

    def to_python(input, tangle = pidgy.tangle.pidgyTransformer()):
        import black, isort
        code = tangle.transform_cell(input)
        code = isort.SortImports(file_contents=code).output
        code = black.format_str(code, mode=black.FileMode(line_length=100))
        return code

    def python(files):
        for file in files:
            code = to_python(pathlib.Path(file).read_text())
            print(highlight_terminal(code, 'python'))

    def markup(files, format='markdown'):
        import nbconvert
        exporter = nbconvert.get_exporter(format)()
        for file in files:
            code = to_markup(pathlib.Path(file).read_text(), exporter)
            print(highlight_terminal(code, format))

    def highlight_terminal(str:str, format='markdown'):


        import pygments.formatters.terminal256
        return pygments.highlight(str, pygments.lexers.find_lexer_class_by_name(format)(), pygments.formatters.terminal256.Terminal256Formatter())

https://stackoverflow.com/questions/34643620/how-can-i-split-my-click-commands-each-with-a-set-of-sub-commands-into-multipl
