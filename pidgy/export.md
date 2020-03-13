Literate programs can be translated into many formats. Commonly markup langauges focus on translation to other markup languages, we add an extra ability to convert markup to source code.

    import pidgy, pathlib, nbformat
    try: from . import util
    except: import util

    def to_markup(input, exporter):
        return exporter.from_notebook_node(input)[0]

    def to_python(input, tangle = pidgy.tangle.pidgyTransformer()):
        import black, isort
        code = tangle.transform_cell(input)
        code = isort.SortImports(file_contents=code).output
        code = black.format_str(code, mode=black.FileMode(line_length=100))
        return code

    def convert(to: {'python', 'markdown'}, files: list, write: bool=False):
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




    def file_to_nb(file: pathlib.Path) -> nbformat.NotebookNode:
        if file.suffix in {'.md', '.markdown'}:
            return nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell(file.read_text())])
        return nbformat.reads(file.read_text(), 4)

https://stackoverflow.com/questions/34643620/how-can-i-split-my-click-commands-each-with-a-set-of-sub-commands-into-multipl
