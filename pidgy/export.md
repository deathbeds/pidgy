# Export documents to other formats.

Literate programs can be translated into many formats. Commonly markup langauges focus on translation to other markup languages, we add an extra ability to convert markup to source code.

    import pidgy, pathlib, typing, textwrap
    try: from . import util
    except: import util

We can reuse existing nbconvert machinery if we expand every file to a notebook.

    def file_to_nb(file: pathlib.Path) -> "nbformat.NotebookNode":
        import nbformat
        if file.suffix in {'.md', '.markdown'}:
            return nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell(file.read_text())])
        return nbformat.reads(file.read_text(), 4)

A notebook can also be flattened.

    def flattennb(nb: typing.Union[str, "nbformat.NotebookNode"]):
        if isinstance(nb, str): return nb
        return [textwrap.indent(''.join(x.source), x.cell_type != 'code' and '# ' or '') for x in nb.cells]

    def to_markup(input: typing.Union[str, "nbformat.NotebookNode"], exporter: "nbconvert.Exporter") -> str:
        return exporter.from_notebook_node(input)[0]

    def to_python(input, tangle = pidgy.loader.pidgyTransformer()):
        import black, isort
        code = tangle.transform_cell(flattennb(input))
        code = isort.SortImports(file_contents=code).output
        code = black.format_str(code, mode=black.FileMode(line_length=100))
        return code

    def convert(*files, to: {'python', 'markdown'}, write: bool=False):
        import nbconvert
        exporter = nbconvert.get_exporter(to)()
        for file in util.yield_files(files):
            nb = file_to_nb(file)
            if to =='python':
                body = '\n'.join(to_python(''.join(getattr(x, 'source', []))) for x in nb.cells)
            else:
                body = to_markup(nb, exporter)
            if write:
                new = pathlib.Path(file).with_suffix(dict(python='.py', markdown='.md')[to])
                new.write_text(body)
                __import__('click').echo(F"{new} created.")
            else:
                __import__('click').echo(body)

https://stackoverflow.com/questions/34643620/how-can-i-split-my-click-commands-each-with-a-set-of-sub-commands-into-multipl
